from validation import format_validator
from utils import config_manager
from utils.logging_setup import detailed_logger, summary_logger
from file_ops import report_tracker
import asyncio, aiohttp

settings = config_manager.load_settings()

async def download_from_queue(
        queue: asyncio.Queue, 
        validation_complete_event: asyncio.Event, 
        timeout: int = settings['timeout']
) -> None:
    sem = asyncio.Semaphore(settings['concurrency_max'])
    async with aiohttp.ClientSession() as session:
        summary_logger.info("Waiting for reports...")
        while not (queue.empty() and validation_complete_event.is_set()):
            if not queue.empty(): summary_logger.info(f"{queue.qsize()} items left in queue...")
            else: summary_logger.info("Waiting for reports...")
            try:
                report = await asyncio.wait_for(queue.get(), timeout=timeout)
                id = report[settings['id_column']]
                validated_url = report['validated_url']
                other_url = report['other_url']
                output_path = settings['output'] / f"{id}.pdf"

                if not settings['retry_failed_download'] and report_tracker.get_report_status(id) == "Download Failed":
                    detailed_logger.info(f"Skipping {id}: marked as a failed download.")
                    queue.task_done()
                    continue

                detailed_logger.debug(f"Downloading {id}...")

                try:
                    success = await download_with_concurrency(sem, session, validated_url, output_path)
                    if success:
                        report_tracker.update_report_status(id, validated_url, other_url, "Downloaded")
                        detailed_logger.debug(f"Completed download of {id}.")
                    else:
                        report_tracker.update_report_status(id, validated_url, other_url, "File Type Mismatch")
                except aiohttp.ClientError as e:
                    detailed_logger.error(f"Failed download of {id}: {e}")
                    report_tracker.update_report_status(id, validated_url, other_url, "Download Failed")

                queue.task_done()
            except asyncio.TimeoutError:
                detailed_logger.debug("Queue wait timed out. Retrying...")
                continue

        summary_logger.info("Download completed.")

async def download_with_concurrency(
        sem: asyncio.Semaphore, 
        session: aiohttp.ClientSession, 
        url: str, 
        output_path: str
) -> bool:
    async with sem:
        return await download(session, url, output_path)

async def download(
        session: aiohttp.ClientSession, 
        url: str, 
        output_path: str
) -> bool:
    try:
        async with session.get(url, ssl=False) as response:
            response.raise_for_status()
            if not format_validator.has_valid_content_type(response):
                detailed_logger.warning(f"Skipping download for {url} due to file type mismatch")
                return False

            with open(output_path, 'wb') as file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)
        return True
    except aiohttp.ClientError as e:
        detailed_logger.error(f"Failed to download {url}: {e}")
        return False

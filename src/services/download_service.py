#services.sync_download_service.py
from validation import format_validator
from utils import config_manager
from utils.logging_setup import detailed_logger, summary_logger
import asyncio, aiohttp

settings = config_manager.load_settings()

async def download_from_queue(queue, validation_complete_event, timeout=settings['timeout']):
    sem = asyncio.Semaphore(settings['concurrency_max'])
    async with aiohttp.ClientSession() as session:
        summary_logger.info("Waiting for reports in the queue...")
        while not (queue.empty() and validation_complete_event.is_set()):
            try:
                report = await asyncio.wait_for(queue.get(), timeout=timeout)
                detailed_logger.debug(f"Retrieved report {report[settings['id_column']]} from queue. Starting download...")

                await download_with_concurrency(
                    sem=sem, 
                    session=session,
                    url=report['validated_url'],
                    output_path=settings['output'] / f"{report[settings['id_column']]}.pdf"
                )
                queue.task_done()
                detailed_logger.debug(f"Completed download for report {report[settings['id_column']]}.")
            except asyncio.TimeoutError:
                detailed_logger.debug("Queue wait timed out. Retrying...")
                continue

        summary_logger.info("Download completed.")

async def download_with_concurrency(sem, session, url, output_path):
    try:
        async with sem:
            detailed_logger.debug(f"Acquired semaphore for downloading {url}. Starting download...")
            await download(session, url, output_path)
            detailed_logger.debug(f"Download finished for {url}. File saved at {output_path}")
    except aiohttp.ClientError as e:
        detailed_logger.error(f"Failed to download {url}: {e}")
        summary_logger.warning(f"Download failed for {url}: {e}")

async def download(session, url, output_path):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            detailed_logger.debug(f"HTTP report successful for {url}. Checking file type...")
            if not format_validator.is_content_type_valid(url, response): return
            detailed_logger.debug(f"File type allowed. Writing...")
            with open(output_path, 'wb') as file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)
            detailed_logger.debug(f"File write complete for {output_path}.")
    except aiohttp.ClientError as e:
        detailed_logger.error(f"HTTP report failed for {url}: {e}")
        raise

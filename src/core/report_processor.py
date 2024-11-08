#core.report_processor.py
from typing import Dict, List
from validation import format_validator
from services import url_ping_service
from utils import config_manager
from utils.logging_setup import detailed_logger, summary_logger
from file_ops import report_tracker
import aiohttp, asyncio

settings = config_manager.load_settings()

async def _validate_and_queue_report(
        sem: asyncio.Semaphore, 
        session: aiohttp.ClientSession, 
        report: List[Dict[str, str]], 
        queue: asyncio.Queue, 
        max_retries: int=settings['max_retries']
) -> None:
    async with sem:
        id_value = report[settings['id_column']]
        primary_url = report[settings['primary_url_column']]
        alternative_url = report[settings['alt_url_column']]

        if report_tracker.is_report_downloaded(id_value):
            detailed_logger.info(f"Skipping {id_value}: Already exists.")
            return
        
        if not settings['retry_unreachable'] and report_tracker.get_report_status(id_value) == "Unreachable":
            detailed_logger.info(f"Skipping {id_value}: marked as unreachable.")
            return

        if format_validator.are_both_urls_invalid(primary_url, alternative_url):
            detailed_logger.warning(f"Skipping {id_value}: Invalid URLs.")
            return

        detailed_logger.info(f"Pinging {id_value}...")   

        retries = 0
        reachable_url = None

        while retries < max_retries and reachable_url is None:
            reachable_url = await url_ping_service.determine_reachable_url(session, primary_url, alternative_url)
        
            if reachable_url is not None:
                detailed_logger.info(f"{id_value} responded: queuing for download.")
                await queue.put({
                    settings['id_column']: id_value,
                    'validated_url': reachable_url,
                    'other_url': primary_url if reachable_url == alternative_url else alternative_url
                })
            else:
                retries += 1
                detailed_logger.warning(f"Retrying {id_value} (attempt {retries}/{max_retries})...")
                await asyncio.sleep(2)

        if reachable_url is None:
            report_tracker.update_report_status(id_value, primary_url, alternative_url, "Unreachable URLs")


async def process_reports(
        reports: List[Dict[str, str]], 
        queue: asyncio.Queue, 
        validation_complete_event: asyncio.Event, 
        max_retries: int=settings['max_retries']
) -> None:
    summary_logger.info(f"Initializing report validation...")
    sem = asyncio.Semaphore(settings['concurrency_max'])
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            _validate_and_queue_report(sem, session, report, queue, max_retries)
            for report in reports
        ]
        await asyncio.gather(*tasks)
    
    validation_complete_event.set()
    summary_logger.info("Validation of all reports completed.")
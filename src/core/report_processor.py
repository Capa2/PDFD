#core.report_processor.py
from validation import format_validator
from services import url_ping_service
from utils import config_manager
from utils.logging_setup import detailed_logger, summary_logger
import aiohttp, asyncio

settings = config_manager.load_settings()

async def validate_and_queue_report(sem, session, report, queue, max_retries=settings['max_retries']):
    async with sem:
        id_value = report[settings['id_column']]
        primary_url = report[settings['primary_url_column']]
        alternative_url = report[settings['alt_url_column']]

        if format_validator.are_both_urls_invalid(primary_url, alternative_url):
            detailed_logger.warning(f"Skipping {id_value} as both URLs are invalid.")
            return

        detailed_logger.info(f"Pinging {id_value}...")   

        retries = 0
        reachable_url = None

        while retries < max_retries and reachable_url is None:
            reachable_url = await url_ping_service.determine_reachable_url(session, primary_url, alternative_url)
        
            if reachable_url is not None:
                detailed_logger.info(f"Validation successful for {id_value}. Adding to download queue.")
                await queue.put({
                    settings['id_column']: id_value,
                    'validated_url': reachable_url,
                    'other_url': primary_url if reachable_url == alternative_url else alternative_url
                })
            else:
                retries += 1
                detailed_logger.warning(f"Retrying validation for {id_value} (attempt {retries}/{max_retries})...")
                await asyncio.sleep(2)

async def process_reports(reports, queue, validation_complete_event, max_retries=settings['max_retries']):
    summary_logger.info("Starting validation of reports...")
    sem = asyncio.Semaphore(settings['concurrency_max'])
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            validate_and_queue_report(sem, session, report, queue, max_retries)
            for report in reports
        ]
        await asyncio.gather(*tasks)
    
    validation_complete_event.set()
    summary_logger.info("Validation of all reports completed.")
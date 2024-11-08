# main.py
from core import report_fetcher, report_processor
from services import download_service
from utils import config_manager
from utils.logging_setup import detailed_logger, summary_logger
import asyncio

settings = config_manager.load_settings()

async def main():
    summary_logger.info("Initializing main process...")

    try:
        reports = report_fetcher.fetch_reports()
        summary_logger.info(f"Found {len(reports)} reports.")
        queue = asyncio.Queue()
        validation_complete_event = asyncio.Event()

        await asyncio.gather(
            report_processor.process_reports(reports, queue, validation_complete_event),
            download_service.download_from_queue(queue, validation_complete_event)
        )
        
        summary_logger.info("Main process completed successfully.")
    except Exception as e:
        detailed_logger.error(f"An error occurred in the main process: {str(e)}", exc_info=True)
        summary_logger.error("Main process failed due to an error.")

if __name__ == "__main__":
    asyncio.run(main())
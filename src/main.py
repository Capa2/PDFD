# main.py
from lib.core import report_fetcher, report_processor
from lib.services import async_download_service
from lib.utils import config_manager
from lib.utils.logging_setup import detailed_logger, summary_logger
import asyncio

settings = config_manager.load_settings()

async def main():
    summary_logger.info("Starting main process...")

    try:
        reports = report_fetcher.fetch_reports()
        detailed_logger.info(f"Retrieved {len(reports)} links to reports.")

        queue = asyncio.Queue()
        validation_complete_event = asyncio.Event()

        await asyncio.gather(
            report_processor.process_reports(reports, queue, validation_complete_event),
            async_download_service.download_from_queue(queue, validation_complete_event)
        )

        summary_logger.info("Main process completed successfully.")
    except Exception as e:
        detailed_logger.error(f"An error occurred in the main process: {e}")
        summary_logger.error("Main process failed due to an error.")

if __name__ == "__main__":
    asyncio.run(main())
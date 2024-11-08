# Mass PDF Download Module

This module is designed to validate and download reports from URLs provided in a spreadsheet, track download statuses, and update an Excel report.

## Overview of Main Components
- src/core/

    - report_processor.py
        - Handles the validation, pinging and queuing of reports for download. It checks if reports have already been downloaded or marked as unreachable and manages retries based on configuration settings.

- src/services/

    - url_ping_service.py
        - Performs reachability checks for URLs. It verifies if URLs are accessible within a timeout and retry limit specified in the configuration and logs the results. It also determines the first reachable URL between primary and alternative URLs.

    - download_service.py
        - Manages the downloading of reports using concurrency. It retrieves reports from the queue, downloads them, and updates the status accordingly.

- src/file_ops/

    - report_fetcher.py
        - Responsible for loading reports from the input spreedsheet file. It fetches report ID and URLs, and applies any configured report limits.
    - report_tracker.py
        - Manages the status tracking of reports in an Excel file. It initializes the report status file if needed and updates or retrieves the status of reports by their ID.

- src/utils/

    - config_manager.py
        - Loads and parses configuration settings from the config.ini file. It provides easy access to paths, column names, and various settings.
    - logging_setup.py
        - Sets up the logging configuration for the application. It initializes detailed and summary loggers, clearing logs on each run and attaches the summery logger to the terminal.

- src/validation/
    
    - format_validator.py
        - Handles content type and URL format validation. It checks if URLs are in a valid format and if the content type of downloaded files is allowed based on the configuration settings.

## Configuration
- config.ini

The config.ini file contains paths, column names, and settings:

- [Paths]: I/O File paths
    - input: Input file from which to retrieve report IDs and URLs
    - output: Output folder for downloads and status report

- [Columns]: Set the column names from the input
    - primary_url_column: Primary download link
    - alt_url_column: Alternative link, will try if primary link is unailable
    - id_column: ID column, used as the output file name, and to check if the report is already downloaded

- [Settings]: Behavioral settings for the program
    - report_limit: How many reports to process. Mostly for debugging
    - concurrency_max: How many threads to run concurrently
    - max_retries: How many attempts to ping each URL in case of failure
    - timeout: How many seconds to wait for a response
    - filetype_whitelist: Which file types are allowed (Currently doesn't work)
    - retry_unreachable: If False, the script will skip reports marked as "Unreachable" in the status report.
    - retry_failed_download: If False, the script will skip reports with previous download failures.

## Usage
To start the validation and download process, edit the config.ini run the main.py script:

    from core import report_fetcher, report_processor
    from services import download_service
    from utils import config_manager
    import asyncio
    
    settings = config_manager.load_settings()
    
    async def main():
        reports = report_fetcher.fetch_reports()
        queue = asyncio.Queue()
        validation_complete_event = asyncio.Event()
    
        await asyncio.gather(
            report_processor.process_reports(reports, queue, validation_complete_event),
            download_service.download_from_queue(queue, validation_complete_event)
        )
    
    if __name__ == "__main__":
        asyncio.run(main())

## Status

An excel sheet is generated in the /out folder, where each processed report is marked as Downloaded, Download Failed or Unreachable URLs

## Logging

The logs reset at every run
- A general overview of the process can be found in /log/summery.log
- A detailed step-by-step as well as precise error logs can be found in /log/detailed.log

#core.report_fetcher.py
from fileops import spreadsheet_reader
from utils import config_manager
from utils.logging_setup import detailed_logger

settings = config_manager.load_settings()

def fetch_reports(
        path=settings["input"], 
        id_field=settings["id_column"], 
        primary_url=settings["primary_url_column"], 
        alternative_url=settings["alt_url_column"], 
        report_limit=settings['report_limit']):
    
    detailed_logger.info("Loading reports from Excel file...")
    reports = spreadsheet_reader.get_dict(path, [id_field, primary_url, alternative_url])
    total_reports = len(reports)
    limited_reports = total_reports if report_limit is None else min(total_reports, report_limit)
    detailed_logger.info(f"Loaded {total_reports} reports. Using {limited_reports} reports for processing.")
    
    return reports if report_limit is None else reports[:report_limit]

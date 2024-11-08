#core.report_fetcher.py
from typing import List, Dict, Optional
from utils import config_manager
from utils.logging_setup import summary_logger, detailed_logger
import pandas as pd

settings = config_manager.load_settings()

def _fetch_dict_from_excel_file(
        path: str, 
        columns: Optional[List[str]]=None
) -> List[Dict[str, str]]:
    try:
        df = pd.read_excel(path, usecols=columns)
        return df.to_dict(orient="records")
    except Exception as e:
        detailed_logger.error(f"Failed to read Excel file {path}: {e}")
        return []

def fetch_reports(
        path: str=settings["input"], 
        id_field: str=settings["id_column"], 
        primary_url: str=settings["primary_url_column"], 
        alternative_url: str=settings["alt_url_column"], 
        report_limit: int=settings['report_limit']
) -> List[Dict[str, str]]:
    
    detailed_logger.info("Loading reports...")
    reports = _fetch_dict_from_excel_file(path, [id_field, primary_url, alternative_url])
    total_reports = len(reports)
    limited_reports = total_reports if report_limit is None else min(total_reports, report_limit)
    summary_logger.info(f"Forwarding {f'{limited_reports}/' if limited_reports else ''}{total_reports} reports.")
    detailed_logger.info(f"Forwarding {f'{limited_reports}/' if limited_reports else ''}{total_reports} reports.")
    
    return reports if report_limit == 0 else reports[:report_limit]

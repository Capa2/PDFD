#io.spreadsheet_reader.py
from typing import List, Dict, Optional
from utils.logging_setup import detailed_logger
import pandas as pd

def get_dict(
        path: str, 
        columns: Optional[List[str]]=None
) -> List[Dict[str, str]]:
    try:
        df = pd.read_excel(path, usecols=columns)
        return df.to_dict(orient="records")
    except Exception as e:
        detailed_logger.error(f"Failed to read Excel file {path}: {e}")
        return []

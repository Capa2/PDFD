#io.spreadsheet_reader.py
from utils.logging_setup import detailed_logger
import pandas as pd

def get_dict(path, columns=None):
    try:
        df = pd.read_excel(path, usecols=columns)
        return df.to_dict(orient="records")
    except Exception as e:
        detailed_logger.error(f"Failed to read Excel file {path}: {e}")
        return []

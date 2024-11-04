# PACKAGES
# requests - For making HTTP requests to download PDF files
# pandas - For reading and processing data from Excel files
# openpyxl - Backend for pandas to read/write .xlsx files
# pypdf - For reading and validating PDF files
# pathlib - Standard library for handling filesystem paths
# logging - Standard library for logging and error tracking
# tqdm - For showing progress bars in the terminal during downloads
# tenacity - For implementing retries with exponential backoff

# main.py
from pathlib import Path
from tabulate import tabulate
import request_handler
import downloader

INPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "GRI_2017_2020.xlsx"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "downloads"

def main():
    valid_requests, invalid_requests = request_handler.validate_and_split(
        path=str(INPUT_PATH), 
        id_field="BRnum", 
        primary_url="Pdf_URL", 
        alternative_url="Report Html Address", 
        limit=20
    )

    print("Valid Requests:")
    print(tabulate(valid_requests, headers="keys"))

    downloader.download_pdfs(valid_requests, OUTPUT_PATH)

if __name__ == "__main__":
    main()
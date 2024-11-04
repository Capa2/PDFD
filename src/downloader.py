import os
import requests
from pathlib import Path
from utils import excel_writer

def download_pdfs(valid_requests, output_folder):
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    for request in valid_requests:
        pdf_id = request['BRnum']
        url = request['Validated_URL']
        output_path = output_folder / f"{pdf_id}.pdf"

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            excel_writer.write_from_iterator(response.iter_content(chunk_size=8192), output_path)
            print(f"Downloaded: {pdf_id}.pdf")
        except requests.RequestException as e:
            print(f"Failed to download {pdf_id}: {e}")

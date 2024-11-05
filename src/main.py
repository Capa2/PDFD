# main.py
import config_loader as config_loader
from tabulate import tabulate
import request_handler
import downloader
import downloader
import asyncio

config = config_loader.load_config()

def main():
    valid_requests, invalid_requests = request_handler.validate_and_split(
        path=config["input"], 
        id_field=config["id_column"], 
        primary_url=config["primary_url_column"], 
        alternative_url=config["alt_url_column"], 
        limit=config["download_limit"]
    )

    print(f"Found {len(valid_requests)} valid URLs. Downloading...\n")
    #print(tabulate(valid_requests, headers="keys"))

    asyncio.run(downloader.download_requests(valid_requests))

if __name__ == "__main__":
    main()
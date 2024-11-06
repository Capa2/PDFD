# main.py
import config_loader as config_loader
from tabulate import tabulate
import request_handler
import asyncio
import downloader

config = config_loader.load_config()

async def main():
    print("Starting main...")

    requests = request_handler.get_requests()

    print(f"Retrieved {len(requests)} requests")

    queue = asyncio.Queue()

    validation_complete_event = asyncio.Event()

    await asyncio.gather(
        request_handler.validate_requests(requests, queue, validation_complete_event),
        downloader.download_from_queue(queue, validation_complete_event)
    )

    print("Main completed")

if __name__ == "__main__":
    asyncio.run(main())
#downloader.py

import requests
import asyncio
import aiohttp
from pathlib import Path
import config_loader

config = config_loader.load_config()

async def download_from_queue(queue, validation_complete_event, timeout=config['timeout']):
    sem = asyncio.Semaphore(config['concurrency_max'])
    async with aiohttp.ClientSession() as session:
        while not (queue.empty() and validation_complete_event.is_set()):
            try:
                request = await asyncio.wait_for(queue.get(), timeout=timeout)
                print("Retrived request from queue. Downloading...")
                await download_with_concurrency(
                    sem=sem, 
                    session=session,
                    url=request['validated_url'],
                    output_path=config['output'] / f"{request[config['id_column']]}.pdf"
                )
                queue.task_done()
                print("Download complete")
            except asyncio.TimeoutError:
                continue

async def download_with_concurrency(sem, session, url, output_path):
    try:
        async with sem:
            await download(session, url, output_path)
    except aiohttp.ClientError as e:
        print(f"Failed to download {url}: {e}")

async def download(session, url, output_path):
    async with session.get(url) as response:
        response.raise_for_status()
        with open(output_path, 'wb') as file:
            while True:
                chunk = await response.content.read(1024)
                if not chunk: break
                file.write(chunk)
    print(f"Downloaded: {output_path}")
#async_downloader.py

import requests
import asyncio
import aiohttp
from pathlib import Path
import config_loader

config = config_loader.load_config()

async def safe_limited_download(sem, session, url, output_path):
    try:
        if sem:
            async with sem:
                await download(session, url, output_path)
        else:
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

async def download_requests(requests):
    sem = asyncio.Semaphore(config['download_limit']) if config['download_limit'] else None
    async with aiohttp.ClientSession() as session:
        tasks = [
            safe_limited_download(
                sem=sem, 
                session=session,  
                url=request['Validated_URL'], 
                output_path=config['output'] / f"{request[config['id_column']]}.pdf"
            )
            for request in requests
        ]

        await asyncio.gather(*tasks)
            
#validator.py
import validators
import aiohttp
import config_loader
import asyncio

config = config_loader.load_config()

def is_valid_url(url):
    return validators.url(url)

async def ping_url(session, url, timeout=config['timeout']):
    try:
        async with session.head(url, timeout=timeout) as response:
            return response.status == 200
    except aiohttp.ClientError:
        return False

async def get_valid_url(session, primary_url, alt_url):
    if not is_valid_url(primary_url) and not is_valid_url(alt_url): return None

    primary_valid, alt_valid = await asyncio.gather(
        ping_url(session, primary_url) if is_valid_url(primary_url) else asyncio.sleep(0),
        ping_url(session, alt_url) if is_valid_url(alt_url) else asyncio.sleep(0),
    )
    
    return primary_url if primary_valid else alt_url if alt_valid else None

def is_valid_id(id):
    return id and len(id) > 0
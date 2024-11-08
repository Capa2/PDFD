#services.url_ping_service.py
from typing import Optional
from validation import format_validator
from utils import config_manager
from utils.logging_setup import detailed_logger
import aiohttp, asyncio

settings = config_manager.load_settings()

async def _check_url_reachability(
        session: aiohttp.ClientSession, 
        url: str, 
        timeout: int=settings['timeout']
) -> bool:
    try:
        detailed_logger.debug(f"Pinging URL: {url:10} with timeout {timeout}")
        async with session.head(url, timeout=timeout, ssl=False) as response:
            result = response.status == 200
            detailed_logger.debug(f"Ping result for {url:10}: {'Success' if result else 'Failed'} (Status: {response.status})")
            return result
    except asyncio.TimeoutError:
        detailed_logger.warning(f"Timeout while pinging {url:10}")
        return False
    except aiohttp.ClientError as e:
        detailed_logger.error(f"Ping failed for {url:10}: {e}")
        return False
    except Exception as e:
        detailed_logger.error(f"Unexpected error while pinging {url:10}: {e}")
        return False

async def determine_reachable_url(
        session: aiohttp.ClientSession, 
        primary_url: str, 
        alt_url: str
) -> Optional[str]:
    detailed_logger.info(f"Validating URLs: {primary_url:10}, {alt_url:10}")
    primary_valid, alt_valid = await asyncio.gather(
        _check_url_reachability(session, primary_url, settings['timeout']) if format_validator.is_valid_url_format(primary_url) else asyncio.sleep(0),
        _check_url_reachability(session, alt_url, settings['timeout']) if format_validator.is_valid_url_format(alt_url) else asyncio.sleep(0),
    )

    if primary_valid:
        detailed_logger.info(f"URL reachable: {primary_url:10}")
        return primary_url
    elif alt_valid:
        detailed_logger.info(f"URL is reachable: {alt_url:10}")
        return alt_url
    else:
        detailed_logger.warning(f"URLs are unreachable: {primary_url:10}, {alt_url:10}")
        return None

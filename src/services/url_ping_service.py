#services.url_ping_service.py
from validation import format_validator
from utils import config_manager
from utils.logging_setup import detailed_logger
import aiohttp, asyncio

settings = config_manager.load_settings()

async def check_url_reachability(session, url, timeout=settings['timeout']):
    try:
        detailed_logger.debug(f"Pinging URL: {url} with timeout {timeout}")
        async with session.head(url, timeout=timeout) as response:
            result = response.status == 200
            detailed_logger.debug(f"Ping result for {url}: {'Success' if result else 'Failed'} (Status: {response.status})")
            return result
    except aiohttp.ClientError as e:
        detailed_logger.error(f"Ping failed for {url}: {e}")
        return False

async def determine_reachable_url(session, primary_url, alt_url):
    detailed_logger.info(f"Validating URLs: Primary - {primary_url}, Alternative - {alt_url}")

    primary_valid, alt_valid = await asyncio.gather(
        check_url_reachability(session, primary_url) if format_validator.is_valid_url_format(primary_url) else asyncio.sleep(0),
        check_url_reachability(session, alt_url) if format_validator.is_valid_url_format(alt_url) else asyncio.sleep(0),
    )

    if primary_valid:
        detailed_logger.info(f"Primary URL is reachable: {primary_url}")
        return primary_url
    elif alt_valid:
        detailed_logger.info(f"Alternative URL is reachable: {alt_url}")
        return alt_url
    else:
        detailed_logger.warning(f"Both URLs are unreachable: {primary_url}, {alt_url}")
        return None

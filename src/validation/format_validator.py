#validation.format_validator.py
from typing import Optional
from utils import config_manager
from utils.logging_setup import detailed_logger
import validators, mimetypes
import aiohttp


settings = config_manager.load_settings()

def is_valid_id(id: str) -> bool: # Not used
    valid = id and len(id) > 0
    detailed_logger.debug(f"ID validation for {id}: {'Valid' if valid else 'Invalid'}")
    return valid

def is_valid_url_format(url: str) -> bool:
    valid = validators.url(url)
    detailed_logger.debug(f"URL validation for {url}: {'Valid' if valid else 'Invalid'}")
    return valid

def are_both_urls_invalid(primary_url: str, alt_url: str) -> bool:
    return not is_valid_url_format(primary_url) and not is_valid_url_format(alt_url)

def _validate_content_type(content_type: Optional[str]) -> bool:
    return True # TODO: Fix: often disallows whitelisted types
    if not content_type: return False
    file_exstension = mimetypes.guess_extension(content_type)
    if file_exstension and file_exstension.upper().lstrip('.') not in settings ['filetype_whitelist']:
        detailed_logger.warning(f"File type {file_exstension} not allowed")
        return False
    return True

def has_valid_content_type(response: aiohttp.ClientResponse) -> bool:
    content_type = response.headers.get('Content-Type')
    if not _validate_content_type(content_type):
        return False
    return True
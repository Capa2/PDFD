#validation.format_validator.py
from utils import config_manager
from utils.logging_setup import detailed_logger
import validators, mimetypes

settings = config_manager.load_settings()

def is_valid_id(id):
    valid = id and len(id) > 0
    detailed_logger.debug(f"ID validation for {id}: {'Valid' if valid else 'Invalid'}")
    return valid

def is_valid_url_format(url):
    valid = validators.url(url)
    detailed_logger.debug(f"URL validation for {url}: {'Valid' if valid else 'Invalid'}")
    return valid

def are_both_urls_invalid(primary_url, alt_url):
    return not is_valid_url_format(primary_url) and not is_valid_url_format(alt_url)

def validate_content_type(content_type):
    if not content_type: return False
    file_exstension = mimetypes.guess_extension(content_type)
    if file_exstension and file_exstension.upper().strip('.') not in settings ['filetype_whitelist']:
        detailed_logger.warning(f"File type {file_exstension} not allowed")
        return False
    return True

def is_content_type_valid(url, response):
    content_type = response.headers.get('Content-Type')
    if not validate_content_type(content_type):
        detailed_logger.warning(f"Skipping download for {url} due to file type mismatch")
        return False
    return True
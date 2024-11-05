#validator.py

import validators
import requests

def is_valid_url(url):
    return validators.url(url)

def ping_url(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException as e:
        return False

def get_valid_url(url, alt_url):
    if is_valid_url(url):
        if ping_url(url):
            return url
    if is_valid_url(alt_url):
        if ping_url(alt_url):
            return alt_url
    return None

def is_valid_id(id):
    return id and len(id) > 0
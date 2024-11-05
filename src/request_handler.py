#request_handler.py

import excel_reader
import validator

def get_requests(path, id_field, primary_url, alternative_url):
    return excel_reader.get_dict(path, [id_field, primary_url, alternative_url])

def validate_and_split(path, id_field, primary_url, alternative_url, limit=None):
    requests = get_requests(path, id_field, primary_url, alternative_url)
    
    valid_requests = []
    invalid_requests = []

    for i, request in enumerate(requests):
        if limit and i >= limit:
            break

        id_value = request[id_field]
        primary_url_value = request[primary_url]
        alternative_url_value = request[alternative_url]

        validated_url = validator.get_valid_url(primary_url_value, alternative_url_value)

        if validated_url is not None:
            valid_requests.append({
                id_field: id_value, 
                'Validated_URL': validated_url, 
                'Secondary_URL': alternative_url_value if validated_url == primary_url_value else primary_url_value
            })
        else:
            invalid_requests.append({
                id_field: id_value, 
                'Primary_URL': primary_url_value, 
                'Alternative_URL': alternative_url_value
            })

    return valid_requests, invalid_requests

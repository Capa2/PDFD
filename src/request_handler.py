#request_handler.py
import excel_reader
import validator
import aiohttp
import asyncio
import config_loader

config = config_loader.load_config()

def get_requests(
        path=config["input"], 
        id_field=config["id_column"], 
        primary_url=config["primary_url_column"], 
        alternative_url=config["alt_url_column"], 
        request_limit=config['request_limit']):
    
    requests = excel_reader.get_dict(path, [id_field, primary_url, alternative_url])
    return requests if request_limit is None else requests[:request_limit]

async def validate_url(sem, session, request, queue, max_retries=config['max_retries']):
    async with sem:
        id_value = request[config['id_column']]
        primary_url_value = request[config['primary_url_column']]
        alternative_url_value = request[config['alt_url_column']]

        print(f"Validating {id_value}...")

        retries = 0
        validated_url = None

        while retries < max_retries and validated_url is None:
            validated_url = await validator.get_valid_url(session, primary_url_value, alternative_url_value)
        
            if validated_url is not None:
                print(f"Validated {id_value}. Adding to queue...")
                await queue.put({
                config['id_column']: id_value,
                'validated_url': validated_url,
                'other_url': primary_url_value if validated_url == alternative_url_value else alternative_url_value
                })

            else:
                retries += 1
                await asyncio.sleep(2)
                print(f"Retrying validation for {id_value} (attempt {retries}/{max_retries}...)")

async def validate_requests(requests, queue, validation_complete_event, max_retries=config['max_retries']):
    print("Validating requests...")
    sem = asyncio.Semaphore(config['concurrency_max'])
    async with aiohttp.ClientSession() as session:
        tasks = [
            validate_url(sem, session, request, queue, max_retries)
            for request in requests
        ]
        await asyncio.gather(*tasks)
    validation_complete_event.set()
    print("Validation complete")
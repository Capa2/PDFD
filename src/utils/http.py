import requests

def get(url):
    response = requests.get(url, stream=True)
    return response

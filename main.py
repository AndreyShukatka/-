import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
token = os.getenv('BITTLY_TOKEN')


def shorten_link(token, url):
    body = {'long_url': url}
    headers = {'Authorization': f'Bearer {token}'}
    url_bitly = 'https://api-ssl.bitly.com/v4/shorten'
    response = requests.post(url_bitly,
                             headers=headers,
                             json=body)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(token, parsed_url):
    headers = {'Authorization': f'Bearer {token}'}
    param = {'units': -1}
    url_bitly = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed_url.netloc}{parsed_url.path}/clicks/summary'
    response = requests.get(url_bitly,
                            headers=headers,
                            params=param)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(parsed_url, token):
    headers = {'Authorization': f'Bearer {token}'}
    url_bitly = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed_url.netloc}{parsed_url.path}'
    response = requests.get(url_bitly,
                            headers=headers)
    return response.ok


def is_valid(parsed_url):
    return bool(parsed_url.netloc) and bool(parsed_url.scheme)


if __name__ == '__main__':
    url = input('Введите ссылку: ')
    parsed_url = urlparse(url)
    if is_bitlink(parsed_url, token):
        print('По вашей ссылке перешли:', count_clicks(token, parsed_url), 'раз(а)')
    elif is_valid(parsed_url):
        print('Битлинк:', shorten_link(token, url))
    else:
        print('Ссылка "', url, '" является нерабочей')

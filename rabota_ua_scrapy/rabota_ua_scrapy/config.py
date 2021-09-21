import os

from .utils.translator_service import TranslatorService

translator_service = TranslatorService()

SEARCH_QUERY = os.environ.get('SEARCH_QUERY')
SEARCH_TOWN = translator_service.translate(os.environ.get('SEARCH_TOWN'))
START_URL = f'https://rabota.ua/zapros/{SEARCH_QUERY}/{SEARCH_TOWN}'
POSTGRESQL_DB = os.environ.get('POSTGRESQL_DB')
POSTGRESQL_USER = os.environ.get('POSTGRESQL_USER')
POSTGRESQL_PASSWORD = os.environ.get('POSTGRESQL_PASSWORD')
POSTGRESQL_CONNECTION_URL = f'postgresql+psycopg2://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@postgres/{POSTGRESQL_DB}'
DOMAIN = 'https://rabota.ua'
HEADERS = {
    'authority': 'rabota.ua',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", '
                 '"Chromium";v="92", '
                 '"Opera";v="78"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'ru-RU,ru;q=0.9,'
                       'en-US;q=0.8,'
                       'en;q=0.7'
}

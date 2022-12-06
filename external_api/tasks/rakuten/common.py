from os import environ

from catalogue.models import Item


HOST = environ['RAKUTEN_URL']

STATIC_HOST = environ['RAKUTEN_STATIC_URL']

IMAGE_HOST = environ['RAKUTEN_IMAGE_URL']

HEADERS = {
    'X-Api-Key': environ['RAKUTEN_API_KEY']
}

PROVIDER_ID = '0006ea0f-724a-4fee-a12f-c6f93300f8b9'

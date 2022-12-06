from os import environ


HOST = environ['RAKUTEN_URL']
STATIC_HOST = environ['RAKUTEN_STATIC_URL']
IMAGE_HOST = environ['RAKUTEN_IMAGE_URL']
HEADERS = {
    'X-Api-Key': environ['RAKUTEN_API_KEY']
}

from os import environ


HOST = environ['RAKUTEN_URL']
STATIC_HOST = environ['RAKUTEN_STATIC_URL']

HEADERS = {
    'X-Api-Key': environ['RAKUTEN_API_KEY']
}

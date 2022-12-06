from os import environ


HOST = environ['RAKUTEN_URL']

HEADERS = {
    'X-Api-Key': environ['RAKUTEN_API_KEY']
}

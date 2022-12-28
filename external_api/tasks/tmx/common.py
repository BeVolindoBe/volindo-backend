from os import environ


HOST = environ['TMX_FLIGHTS_URL']

X_USERNAME = environ['TMX_X_USERNAME']
X_DOMAIN_KEY = environ['TMX_X_DOMAIN_KEY']
X_SYSTEM = environ['TMX_X_SYSTEM']
X_PASSWORD = environ['TMX_X_PASSWORD']

SEARCH_URL = f'{HOST}/Search'

PROVIDER_ID = '06c0c84a-af8b-4c0f-b5c3-891c53e492f2'

HEADERS = {
    'x-Username': X_USERNAME,
    'x-DomainKey': X_DOMAIN_KEY,
    'x-system': X_SYSTEM,
    'x-Password': X_PASSWORD,
    'Content-Type': 'application/json',
	'User-Agent': 'Mozilla/5.0'
}

from os import environ

from catalogue.models import Item


HOST = environ['TBO_URL']
AUTH = environ['TBO_AUTH']

SEARCH_URL = f'{HOST}/Search'

HEADERS = {
	'Authorization': f'Basic {AUTH}',
	'Content-Type': 'application/json'
}

PROVIDER_ID = 'a33ba54c-34f9-4f1a-9d87-0d85a4cfdeba'

EXPECTED_RESPONSE_TIME=int(environ['TBO_EXPECTED_RESPONSE_TIME'])

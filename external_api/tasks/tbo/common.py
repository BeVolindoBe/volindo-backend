from os import environ

from catalogue.models import Item


HOST = environ['TBO_URL']

# STATIC_HOST = environ['RAKUTEN_STATIC_URL']

# IMAGE_HOST = environ['RAKUTEN_IMAGE_URL']

HEADERS = {
	'Authorization': 'Basic Vm9saW5kb214VGVzdDpWb2xAMjU0MDY3OTQ=',
	'Content-Type': 'application/json'
}

PROVIDER_ID = 'a33ba54c-34f9-4f1a-9d87-0d85a4cfdeba'

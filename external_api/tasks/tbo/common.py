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

EXPECTED_SEARCH_RESPONSE_TIME=int(environ['TBO_EXPECTED_SEARCH_RESPONSE_TIME'])
EXPECTED_DETAIL_RESPONSE_TIME=int(environ['TBO_EXPECTED_DETAIL_RESPONSE_TIME'])


def parse_rooms(rooms_list) -> list:
	rooms = []
	for room in rooms_list:
		rooms.append({
			'Adults': room['number_of_adults'],
			'Children': len(room['children_age']),
			'ChildrenAges': room['children_age']
		})
	return rooms


def parse_hotels(hotels) -> dict:
	"""
		Hotels tuple were the internal id is the first element
		and the external is the second one
	"""
	external_ids = []
	ids = ''
	hotels_dict = {}
	for h in hotels:
		external_ids.append(h[1])
		ids = ids + f'{h[1]},'
		hotels_dict[h[1]] = {
			'id': str(h[0])
		}
	parsed_hotels = {
		'ids': ids[:-1],
		'external_ids': external_ids,
		'hotels_dict': hotels_dict
	}
	return parsed_hotels

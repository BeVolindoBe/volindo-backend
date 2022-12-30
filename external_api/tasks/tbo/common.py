from os import environ


HOST = environ['TBO_URL']
AUTH = environ['TBO_AUTH']

BATCH = int(environ['BATCH_HOTEL_SEARCH'])

SEARCH_URL = f'{HOST}/Search'
PREBOOK_URL = f'{HOST}/PreBook'
BOOK_URL = f'{HOST}/Book'
BOOKING_DETAIL_URL = f'{HOST}/BookingDetail'

HEADERS = {
	'Authorization': f'Basic {AUTH}',
	'Content-Type': 'application/json'
}

PROVIDER_ID = 'a33ba54c-34f9-4f1a-9d87-0d85a4cfdeba'

PAYMENT_TYPE = '2f0d3a9b-22de-40ca-a701-b5a5b36a04ba'

PAYMENT_METHOD = 'Limit' if environ['TBO_PAYMENT_METHOD'] == 'LIMIT' else 'Credit Card'

EXPECTED_SEARCH_RESPONSE_TIME = float(environ['TBO_EXPECTED_SEARCH_RESPONSE_TIME'])
EXPECTED_DETAIL_RESPONSE_TIME = float(environ['TBO_EXPECTED_DETAIL_RESPONSE_TIME'])

REQUEST_BATCH = int(environ['REQUEST_BATCH'])


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

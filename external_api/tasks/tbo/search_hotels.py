import json

import requests

from django.core.cache import cache

from celery import shared_task

from external_api.tasks.tbo.common import HEADERS, SEARCH_URL, EXPECTED_RESPONSE_TIME

from hotel.models import Hotel


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


@shared_task
def search_tbo(results_id, filters):
	parsed_rooms = parse_rooms(filters['rooms'])
	hotels = Hotel.objects.values_list('id', 'external_id').filter(destination_id=filters['destination'])
	parsed_hotels = parse_hotels(hotels=hotels)
	parsed_hotels['ids']
	payload = {
		'CheckIn': filters['check_in'], # format YYYY-mm-dd
		'CheckOut': filters['check_out'], # format YYYY-mm-dd
		'HotelCodes': parsed_hotels['ids'],
		'GuestNationality': filters['nationality'],
		'PaxRooms': parsed_rooms,
		'ResponseTime': EXPECTED_RESPONSE_TIME,
		'IsDetailedResponse': False
	}
	response = requests.post(SEARCH_URL, headers=HEADERS, data=json.dumps(payload))
	if response.status_code == 200:
		temp_hotels = []
		for hotel in response.json()['HotelResult']:
			temp = parsed_hotels['hotels_dict'][hotel['HotelCode']]
			temp['price'] = hotel['Rooms'][0]['TotalFare']
			temp_hotels.append(temp)
		results = json.loads(cache.get(results_id))
		results['status'] = 'update'
		results['hotels'].extend(temp_hotels)
		# results['hotels'].sort(key=price)
		cache.set(results_id, json.dumps(results), 18000)

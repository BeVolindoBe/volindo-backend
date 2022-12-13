import json

import requests

from django.core.cache import cache

from celery import shared_task

from external_api.tasks.tbo.common import(
	HEADERS, SEARCH_URL, EXPECTED_SEARCH_RESPONSE_TIME, parse_hotels, parse_rooms
)

from hotel.models import Hotel


def process(hotels, parsed_rooms, results_id, filters):
	parsed_hotels = parse_hotels(hotels=hotels)
	payload = {
		'CheckIn': filters['check_in'], # format YYYY-mm-dd
		'CheckOut': filters['check_out'], # format YYYY-mm-dd
		'HotelCodes': parsed_hotels['ids'],
		'GuestNationality': filters['nationality'],
		'PaxRooms': parsed_rooms,
		'ResponseTime': EXPECTED_SEARCH_RESPONSE_TIME,
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
		cache.set(results_id, json.dumps(results), 18000)


@shared_task
def search_tbo(results_id, filters):
	parsed_rooms = parse_rooms(filters['rooms'])
	hotels = Hotel.objects.values_list('id', 'external_id').filter(
		destination_id=filters['destination']
	)
	counter = 0
	batch = 10
	while counter <= len(hotels):
		process(hotels[counter:counter+batch], parsed_rooms, results_id, filters)
		counter += batch

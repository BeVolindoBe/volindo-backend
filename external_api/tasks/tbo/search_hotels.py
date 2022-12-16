import json

import requests

from django.core.cache import cache

from celery import shared_task

from external_api.tasks.tbo.common import(
    HEADERS, SEARCH_URL, EXPECTED_SEARCH_RESPONSE_TIME,
    parse_hotels, parse_rooms
)

from hotel.models import Hotel


@shared_task
def tbo_search_hotels(results_id, filters):
    parsed_rooms = parse_rooms(filters['rooms'])
    hotels = Hotel.objects.values_list('id', 'external_id').filter(
        destination_id=filters['destination']
    )
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
    hotels = response.json()['HotelResult']
    temp_hotels = []
    for hotel in hotels:
        temp = parsed_hotels['hotels_dict'][hotel['HotelCode']]
        temp['price'] = hotel['Rooms'][0]['TotalFare']
        temp_hotels.append(temp)
    results = json.loads(cache.get(results_id))
    results['hotels'] = []
    results['hotels'].extend(temp_hotels)
    results['status'] = 'update'
    cache.set(results_id, json.dumps(results), 18000)

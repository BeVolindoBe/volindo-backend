import json

import requests

from django.core.cache import cache

from celery import shared_task

from external_api.logs import save_log
from external_api.tasks.tbo.common import(
    HEADERS, SEARCH_URL, EXPECTED_SEARCH_RESPONSE_TIME,
    parse_hotels, parse_rooms, PROVIDER_ID, BATCH
)

from hotel.models import Hotel
from hotel.serializers import HotelSerializer


@shared_task
def fetch_hotel_data(hotels_list, filters, parsed_rooms, results_id):
    payload = {
        'CheckIn': filters['check_in'], # format YYYY-mm-dd
        'CheckOut': filters['check_out'], # format YYYY-mm-dd
        'HotelCodes': ','.join(hotels_list.keys()), # 100043,32412443
        'GuestNationality': filters['nationality'],
        'PaxRooms': parsed_rooms,
        'ResponseTime': EXPECTED_SEARCH_RESPONSE_TIME,
        'IsDetailedResponse': False
    }
    response = requests.post(SEARCH_URL, headers=HEADERS, data=json.dumps(payload))
    data = response.json()
    save_log(PROVIDER_ID, SEARCH_URL, payload, response.status_code, response.json())
    if response.status_code == 200 and data['Status']['Code'] == 200:
        hotels = Hotel.objects.prefetch_related(
            'hotel_amenities', 'hotel_pictures'
        ).filter(external_id__in=hotels_list.keys())
        for h in hotels:
            hotels_list[h.external_id] = HotelSerializer(h).data
        prices = data['HotelResult']
        for p in prices:
            hotels_list[p['HotelCode']]['price'] = p['Rooms'][0]['TotalFare']
        results = json.loads(cache.get(results_id))
        results['hotels'].extend(hotels_list.values())
        results['status'] = 'update'
        cache.set(results_id, json.dumps(results), 900)


@shared_task
def tbo_search_hotels(results_id, filters):
    parsed_rooms = parse_rooms(filters['rooms'])
    hotels = Hotel.objects.values_list('external_id').filter(
        destination_id=filters['destination']
    )
    counter = 0
    while counter <= len(hotels):
        hotels_list = {
            h[0]: {} for h in hotels[counter:counter+BATCH]
        }
        fetch_hotel_data.delay(hotels_list, filters, parsed_rooms, results_id)
        counter += BATCH

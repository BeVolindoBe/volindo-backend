import json

import requests

from django.core.cache import cache

from rest_framework import status

from common.response_class import GenericResponse
from common.common import get_number_of_nights

from external_api.tasks.tbo.common import(
    HEADERS, SEARCH_URL, EXPECTED_DETAIL_RESPONSE_TIME, parse_rooms
)

from hotel.models import Hotel
from hotel.serializers import HotelSerializer


def parse_hotel_detail(data):
    return [
        {
            'name': r['Name'][0],
            'booking_code': r['BookingCode'],
            'price': r['TotalFare'],
            'amenities': [
                {
                    'amenity': a
                } for a in r['Inclusion'].split(',')
            ]
        } for r in data['Rooms']
    ]


def tbo_hotel_details(hotel_id, results_id):
    results = cache.get(results_id)
    if results is None:
        data = GenericResponse(
            data={'message': 'Hotel data not longer available.'},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
        return data
    filters = json.loads(cache.get(results_id))['filters']
    parsed_rooms = parse_rooms(filters['rooms'])
    hotel_data = HotelSerializer(
        Hotel.objects.prefetch_related('hotel_pictures', 'hotel_amenities').get(id=hotel_id)
    ).data
    payload = {
		'CheckIn': filters['check_in'], # format YYYY-mm-dd
		'CheckOut': filters['check_out'], # format YYYY-mm-dd
		'HotelCodes': hotel_data['external_id'],
		'GuestNationality': filters['nationality'],
		'PaxRooms': parsed_rooms,
		'ResponseTime': EXPECTED_DETAIL_RESPONSE_TIME,
		'IsDetailedResponse': False
    }
    response = requests.post(SEARCH_URL, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 200:
        hotel = {
            'rooms': [],
            'number_of_nights': get_number_of_nights(filters['check_in'], filters['check_out']),
            'results_id': results_id
        }
        if 'HotelResult' in response.json():
            hotel['rooms'] = parse_hotel_detail(response.json()['HotelResult'][0])
        hotel.update(hotel_data)
        data = GenericResponse(data=hotel, status_code=status.HTTP_200_OK)
    else:
        data = GenericResponse(
            data={'message': 'Unable to get hotel information.'},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    return data

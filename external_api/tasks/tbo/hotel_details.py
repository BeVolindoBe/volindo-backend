import json

import requests

from django.core.cache import cache
from django.forms.models import model_to_dict

from rest_framework import status

from common.response_class import GenericResponse

from external_api.tasks.tbo.common import(
    HEADERS, SEARCH_URL, EXPECTED_DETAIL_RESPONSE_TIME, parse_rooms
)

from hotel.models import Hotel


def parse_hotel_detail(data):
    return [
        {
            'name': r['Name'],
            'booking_code': r['BookingCode'],
            'price': r['TotalFare'] + r['TotalTax'],
            'amenities': r['Inclusion'].split(',')
        } for r in data['Rooms']
    ]


def tbo_hotel_details(hotel_id, results_id):
    filters = json.loads(cache.get(results_id))['filters']
    parsed_rooms = parse_rooms(filters['rooms'])
    hotel = model_to_dict(Hotel.objects.get(id=hotel_id))
    payload = {
		'CheckIn': filters['check_in'], # format YYYY-mm-dd
		'CheckOut': filters['check_out'], # format YYYY-mm-dd
		'HotelCodes': hotel['external_id'],
		'GuestNationality': filters['nationality'],
		'PaxRooms': parsed_rooms,
		'ResponseTime': EXPECTED_DETAIL_RESPONSE_TIME,
		'IsDetailedResponse': False
    }
    response = requests.post(SEARCH_URL, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 200:
        hotel['rooms'] = parse_hotel_detail(response.json()['HotelResult'][0])
        data = GenericResponse(data=hotel, status_code=status.HTTP_200_OK)
    else:
        data = GenericResponse(
            data={'message': 'Unable to get hotel information.'},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    return data

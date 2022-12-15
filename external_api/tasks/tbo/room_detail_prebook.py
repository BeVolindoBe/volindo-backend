import json

from datetime import datetime

import requests

from django.core.cache import cache

from rest_framework import status

from common.response_class import GenericResponse
from common.common import get_number_of_nights

from external_api.tasks.tbo.common import(
    HEADERS, PREBOOK_URL, PAYMENT_MODE
)


def get_room_price(prices):
    price = 0
    for p in prices:
        price += p['BasePrice']
    return round(price, 2)


def parse_rooms(rooms):
    data = {
        'price': rooms[0]['TotalFare'],
        'tax': rooms[0]['TotalTax'],
        'cancel_policies': [
            {
                'from_date': datetime.strptime(c['FromDate'], '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d'), # 12-12-2022 00:00:00
                'charge': c['CancellationCharge']
            } for c in rooms[0]['CancelPolicies']
        ],
        'booking_code': rooms[0]['BookingCode'],
        'rooms_details': [
            {
                'name': rooms[0]['Name'][x],
                'price': get_room_price(rooms[0]['DayRates'][x])
            } for x in range(len(rooms[0]['Name']))
        ]
    }
    return data


def tbo_room_prebook_details(details):
    results = cache.get(details['results_id'])
    if results is None:
        response = GenericResponse(
            data={'message': 'Hotel data is not longer available.'},
            status_code=status.HTTP_404_NOT_FOUND
        )
        return response
    payload = {
        'BookingCode': details['booking_code'],
        'PaymentMode': PAYMENT_MODE
    }
    results = json.loads(results)
    prebook = requests.post(PREBOOK_URL, headers=HEADERS, data=json.dumps(payload))
    if prebook.status_code == 200:
        prebook_data = prebook.json()
        # print(prebook_data)
        if 'HotelResult' in prebook_data:
            policies = prebook_data['HotelResult'][0]['RateConditions'] if 'RateConditions' in prebook_data['HotelResult'][0] else []
            data = {
                'filters': results['filters'],
                'number_of_nights': get_number_of_nights(results['filters']['check_in'], results['filters']['check_out']),
                'policies': policies,
                'rooms': parse_rooms(prebook_data['HotelResult'][0]['Rooms'])
            }   
            response = GenericResponse(
                data=data,
                status_code=status.HTTP_200_OK
            )
            return response
        else:
            response = GenericResponse(
                data={'message': 'Hotel data is not longer available.'},
                status_code=status.HTTP_404_NOT_FOUND
            )
            return response

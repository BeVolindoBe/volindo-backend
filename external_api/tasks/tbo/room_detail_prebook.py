import json

from datetime import datetime

import requests

from django.core.cache import cache

from rest_framework import status

from common.response_class import GenericResponse
from common.common import get_number_of_nights

from external_api.logs import save_log
from external_api.tasks.tbo.common import(
    HEADERS, PREBOOK_URL, PROVIDER_ID, PAYMENT_METHOD
)


SUPPLEMENTS_DICT = {
    'AtProperty': 'At property',
    'Included': 'Included'
}


def get_room_price(prices):
    price = 0
    for p in prices:
        price += p['BasePrice']
    return round(price, 2)


def get_supplements(room):
    return [
        {
            'type': SUPPLEMENTS_DICT[s['Type']],
            'price': f"{s['Price']} {s['Currency']}",
            'description': s['Description'].replace('_', ' ').capitalize()
        } for s in room
    ]


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
                'price': get_room_price(rooms[0]['DayRates'][x]),
                'supplements': get_supplements(rooms[0]['Supplements'][x]) if 'Supplements' in rooms[0] else []
            } for x in range(len(rooms[0]['Name']))
        ]
    }
    return data


def tbo_get_room_prebook_details(details):
    results = cache.get(details['results_id'])
    if results is None:
        response = GenericResponse(
            data={'message': 'Hotel data is not longer available.'},
            status_code=status.HTTP_404_NOT_FOUND
        )
        return response
    payload = {
        'BookingCode': details['booking_code'],
        'PaymentMode': PAYMENT_METHOD
    }
    results = json.loads(results)
    prebook = requests.post(PREBOOK_URL, headers=HEADERS, data=json.dumps(payload))
    save_log(PROVIDER_ID, PREBOOK_URL, payload, prebook.status_code, prebook.json())
    if prebook.status_code == 200:
        prebook_data = prebook.json()
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

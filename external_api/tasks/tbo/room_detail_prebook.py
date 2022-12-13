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


def tbo_room_prebook_details(details):
    """
    data: {
        hotel_id
        results_id
        booking_code
        hotel_name
    }
    """
    results = cache.get(details['results_id'])
    if results is None:
        response = GenericResponse(
            data={'message': 'Hotel data not longer available.'},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
        return response
    payload = {
        'BookingCode': details['booking_code'],
        'PaymentMode': PAYMENT_MODE
    }
    results = json.loads(results)
    prebook = requests.post(PREBOOK_URL, headers=HEADERS, data=json.dumps(payload))
    room = prebook.json()['HotelResult'][0]['Rooms'][0]
    try:
        policies = room['RateConditions']
    except KeyError:
        policies = []
    data = {
        'filters': results['filters'],
        'hotel_id': details['hotel_id'],
        'hotel_name': details['hotel_name'],
        'number_of_nights': get_number_of_nights(results['filters']['check_in'], results['filters']['check_out']),
        'policies': policies,
        'name': room['Name'][0],
        'price': room['TotalFare'],
        'booking_code': room['BookingCode'],
        'cancel_policies': [
            {
                'from_date': datetime.strptime(c['FromDate'], '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d'), # 12-12-2022 00:00:00
                'charge': c['CancellationCharge']
            } for c in room['CancelPolicies']
        ]
    }   
    response = GenericResponse(
        data=data,
        status_code=status.HTTP_200_OK
    )
    return response

from os import environ

import json

import requests

from django.core.cache import cache

from celery import shared_task


credentials = {
    'host': environ['TBO_SEARCH_URL'],
    'username': environ['TBO_USERNAME'],
    'password': environ['TBO_PASSWORD']
}


# def parse(cache_key, filter):
#     results = json.loads(cache.get(cache_key))
#     for hotel in data:
#         results['hotels'].append(
#             {
#                 'provider': 'Booking',
#                 'name': hotel['hotel_name'],
#                 'offered_price': float(hotel['price_breakdown']['all_inclusive_price']),
#                 'total_price': float(hotel['price_breakdown']['gross_price']),
#                 'image': hotel['main_photo_url'],
#                 'star_rating': int(hotel['class']),
#                 'latitude': float(hotel['latitude']),
#                 'longitude': float(hotel['longitude']),
#                 'amenities': []
#             }
#         )
#     results['hotels'].sort(key=lambda x: x['total_price'])
#     cache.set(cache_key, json.dumps(results), 900)


def parse_filters(filters):
    return {
        'CheckIn': filters['check_in'],
        'CheckOut': filters['check_out'],
        'HotelCodes': '1247101',
        'GuestNationality': filters['nationality'],
        'PaxRooms': [
            {
                'Adults': filters['adults'],
                'Children': filters['children'],
                'ChildrenAges': [1]
            }
        ],
        'ResponseTime': 23.0,
        'IsDetailedResponse': False,
        'Filters': {
            'Refundable': False,
            'NoOfRooms': 0,
            'MealType': 'ALL'
        }
    }


@shared_task
def search_hotels_tbo(cache_key, filters):
    parsed_filters = parse_filters(filters)
    response = requests.post(
        credentials['host'],
        auth=(credentials['username'], credentials['password']),
        data=parse_filters

    )
    print(response.status_code, response.data)

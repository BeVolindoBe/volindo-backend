import json

import requests

from django.core.cache import cache

from celery import shared_task


def parse(data, cache_key):
    results = json.loads(cache.get(cache_key))
    for hotel in data:
        results['hotels'].append(
            {
                'provider': 'Booking',
                'name': hotel['hotel_name']
            }
        )
    cache.set(cache_key, json.dumps(results), 900)


@shared_task
def fetch_from_booking():
    url = 'https://apidojo-booking-v1.p.rapidapi.com/properties/list'
    querystring = {
        'offset':'0',
        'arrival_date':'2022-12-01',
        'departure_date':'2022-12-06',
        'guest_qty':'1',
        'dest_ids':'-3712125',
        'room_qty':'1',
        'search_type':'city',
        'children_qty':'2',
        'children_age':'5,7',
        'search_id':'none',
        'price_filter_currencycode':'USD',
        'order_by':'popularity',
        'languagecode':'en-us',
        'travel_purpose':'leisure'
    }
    headers = {
        'X-RapidAPI-Key': '2809f2479dmsh2cc896f7aa81a16p17b41fjsn3a20378de8b2',
        'X-RapidAPI-Host': 'apidojo-booking-v1.p.rapidapi.com'
    }
    response = requests.request('GET', url, headers=headers, params=querystring)
    data = response.json()['result']
    parse(data, 'test')
    with open('booking.json', 'w') as f:
        f.write(json.dumps(data, indent=4))
        f.close()
    print(f'Booking response is ready with {len(data)} results'.upper())

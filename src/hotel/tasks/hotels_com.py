import json

import requests

from django.core.cache import cache

from celery import shared_task


def parse(data, cache_key):
    results = json.loads(cache.get(cache_key))
    for hotel in data:
        results['hotels'].append(
            {
                'provider': 'Hotel.com',
                'name': hotel['name']
            }
        )
    cache.set(cache_key, json.dumps(results), 900)


@shared_task
def fetch_from_hotels_com():
    url = 'https://hotels-com-provider.p.rapidapi.com/v1/destinations/search'
    querystring = {'query':'London','currency':'USD','locale':'en_US'}
    headers = {
        'X-RapidAPI-Key': '2809f2479dmsh2cc896f7aa81a16p17b41fjsn3a20378de8b2',
        'X-RapidAPI-Host': 'hotels-com-provider.p.rapidapi.com'
    }
    response = requests.request('GET', url, headers=headers, params=querystring)
    data = response.json()['suggestions'][1]['entities']
    parse(data, 'test')
    with open('hotels_com.json', 'w') as f:
        f.write(json.dumps(data, indent=4))
        f.close()
    print(f'Hotels.com response is ready with {len(data)} results'.upper())

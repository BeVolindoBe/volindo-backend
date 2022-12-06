import json

import requests

from django.core.cache import cache

from celery import shared_task

from external_api.tasks.rakuten.common import HEADERS, STATIC_HOST, IMAGE_HOST


def save_data(hotels):
    image_url = url = IMAGE_HOST + '/{}/{}' # hotel id then image file name
    hotels_id = []
    for k, v in hotels.items():
        print(k, v)
        break


def get_properties():
    url = STATIC_HOST + '/my-property-list'
    properties = requests.get(
        url=url,
        headers=HEADERS
    )
    return [
        p['property_code'] for p in properties.json()['my_property_list']
    ]


def get_details(properties_codes):
    url = STATIC_HOST + '/properties?extends=long%2Cimages%2Crooms%2Cfacilities'
    body = {
        'property_codes': properties_codes
    }
    details = requests.post(
        url=url,
        headers=HEADERS,
        data=json.dumps(body)
    )
    return details.json()


def rakuten_data():
    proprties = get_properties()
    hotels = get_details(properties_codes=proprties)
    save_data(hotels=hotels)

import json

import requests

from django.core.cache import cache

from celery import shared_task

from external_api.tasks.rakuten.common import HEADERS, STATIC_HOST


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
    print(json.dumps(details.json(), indent=4))


def rakuten_data():
    proprties = get_properties()
    get_details(properties_codes=proprties)

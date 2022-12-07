import json

import requests

from django.core.cache import cache

from celery import shared_task

from catalogue.models import Item

from external_api.tasks.rakuten.common import HEADERS, HOST, PROVIDER_ID

from hotel.models import Hotel


QUERY_STRING = '/hotel_list?adult_count={}&check_in_date={}&check_out_date={}&children={}&currency={}&hotel_id_list={}&room_count={}&source_market={}&child_count={}'


def parse_rooms(rooms_list) -> dict:
    adults = 0
    child_count = 0
    children = ''
    for obj in rooms_list:
        adults += obj['number_of_adults'] 
        for c in obj['children_age']:
            child_count += 1
            children = children + str(c) + ','
    return {
        'adults': adults,
        'children': children[:-1],
        'child_count': child_count
    }


@shared_task
def search_rakuten(results_id, filters):
    destination = Item.objects.get(id=filters['destination'])
    parsed_rooms = parse_rooms(filters['rooms'])
    hotels = Hotel.objects.prefetch_related('hotel_pictures').filter(
        provider_id=PROVIDER_ID,
        destination_id=destination
    )
    url = HOST + QUERY_STRING.format(
        parsed_rooms['adults'],
        filters['check_in'],
        filters['check_out'],
        parsed_rooms['children'],
        filters['currency'],
        'KQQR,reFn,usg1',
        len(filters['rooms']),
        filters['nationality'],
        parsed_rooms['child_count']
    )
    response = requests.get(
        url,
        headers=HEADERS
    )
    print(response.json())

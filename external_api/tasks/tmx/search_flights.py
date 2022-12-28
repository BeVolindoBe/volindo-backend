import json

import requests

from django.core.cache import cache

from celery import shared_task

from external_api.logs import save_log
from external_api.tasks.tmx.common import(
    HEADERS, SEARCH_URL, PROVIDER_ID
)


@shared_task
def tmx_search_flights(results_id, filters):
    payload = {
        'AdultCount': f"{filters['adults']}",
        'ChildCount': f"{filters['children']}",
        'InfantCount': f"{filters['infants']}",
        'JourneyType': f"{filters['flight_type']}",
        'PreferredAirlines': [''],
        'CabinClass': f"{filters['flight_class']}",
        'Segments': [
            {
                'Origin': 'BLR',
                'Destination': 'MAA',
                'DepartureDate': '2023-01-04T00:00:00',
                'ReturnDate': '2023-01-10T00:00:00'
            }
        ]
    }
    print(SEARCH_URL)
    response = requests.post(SEARCH_URL, headers=HEADERS, data=json.dumps(payload))
    print(response.text)
    # print(response.json())
    save_log(PROVIDER_ID, SEARCH_URL, payload, response.status_code, response.json())
    results = json.loads(cache.get(results_id))
    results['flights'] = []
    results['status'] = 'update'
    cache.set(results_id, json.dumps(results), 900)

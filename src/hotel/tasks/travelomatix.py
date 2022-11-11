import json

import requests

from django.core.cache import cache

from celery import shared_task


@shared_task
def fetch_from_travelomatix():
    url = 'http://test.services.travelomatix.com/webservices/index.php/hotel_v3/service/Search'
    headers = {
            'x-Username': 'test273344',
            'x-DomainKey': 'TMX5262731660138834',
            'x-system': 'test',
            'x-Password': 'test@273',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
    body = {
        'CheckInDate': '01-12-2022',
        'NoOfNights': 5,
        'CountryCode': 'MX',
        'CityId': 424,
        'GuestNationality': 'MX',
        'NoOfRooms': 1,
        'RoomGuests': [
            {
                'NoOfAdults': 1,
                'NoOfChild': 0
            }
        ]
    }
    response = requests.post(
        url,
        data=json.dumps(body),
        headers=headers
    )
    data = response.json()['Search']['HotelSearchResult']['HotelResults']
    cache.set('travelomatix', json.dumps(data), 600)
    with open('travelomatix.json', 'w') as f:
        f.write(json.dumps(data, indent=4))
        f.close()
    print(f'Travelomatix response is ready with {len(data)} results'.upper())

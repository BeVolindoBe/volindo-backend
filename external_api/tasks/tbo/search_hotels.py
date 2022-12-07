import json
import requests
from django.core.cache import cache
from celery import shared_task
from external_api.tasks.tbo.common import HEADERS, HOST, PROVIDER_ID
from hotel.models import Hotel

def parse_rooms(rooms_list) -> list:
    rooms = []
    for room in rooms_list:
        rooms.append({
            'Adults': room['number_of_adults'],
            'Children': len(room['children_age']),
            'ChildrenAges': room['children_age']
        })
    return rooms


@shared_task
def search_tbo(results_id, filters):
    url = f'{HOST}/Search'
    parsed_rooms = parse_rooms(filters['rooms'])

    payload = {
      'CheckIn': filters['check_in'], # format YYYY-mm-dd
      'CheckOut': filters['check_out'], # format YYYY-mm-dd
      'HotelCodes': '1000000,1000001,1000002,1000003,1000004,1000005,1000006,1000007,1000008,1000009,1000011,1000012',
      'GuestNationality': filters['nationality'],
      'PaxRooms': parsed_rooms,
      'ResponseTime': 23,
      'IsDetailedResponse': False
    }

    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 200:
      response = response.json()
      ids = [hotel['HotelCode'] for hotel in response['HotelResult']]

      searchedHotels = Hotel.objects.filters(provider_id='a33ba54c-34f9-4f1a-9d87-0d85a4cfdeba', external_id__in=ids)
      for index, hotel in enumerate(searchedHotels):
        hotel['price'] = response['HotelResult'][index]['Rooms'][0]['TotalFare']
      

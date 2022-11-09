from os import environ

import threading

from multiprocessing.pool import ThreadPool

import json

import requests

from django.core.management.base import BaseCommand

from catalogue.models import Item

from hotel.models import Hotel

from task.logging import log


def save_data(token):
    data = {
        'CheckInDate': '01-12-2022',
        'NoOfNights': 5,
        'CountryCode': 'MX',
        'CityId': 424,
        'GuestNationality': 'EC',
        'NoOfRooms': 1,
        'RoomGuests': [
            {
                'NoOfAdults': 2,
                'NoOfChild': 0
            }
        ]
    }
    try:
        r = requests.post(
            'http://test.services.travelomatix.com/webservices/index.php/hotel_v3/service/HotelDetails',
            data=json.dumps(
                {
                    'ResultToken': token
                }
            ),
            headers={
                'x-Username': environ.get('TMTX_USERNAME'),
                'x-DomainKey': environ.get('TMTX_DOMAINKEY'),
                'x-system': environ.get('TMTX_SYSTEM'),
                'x-Password': environ.get('TMTX_PASSWORD'),
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            }
        )
        return Hotel(
            destination=data['CityId'],
            check_in_date=data['CheckInDate'],
            number_of_rooms=data['NoOfRooms'],
            number_of_adults=data['RoomGuests'][0]['NoOfAdults'],
            number_of_nights=data['NoOfRooms'],
            number_of_child=data['RoomGuests'][0]['NoOfChild'],
            hotel_info=r.json()
        )
    except requests.exceptions.RequestException as e:
        log('Unable to get data from the API: {}'.format(e))
    except KeyError as e:
        log(e)



class Command(BaseCommand):

    help = ''

    def __init__(self):
        self.headers = {
            'x-Username': environ.get('TMTX_USERNAME'),
            'x-DomainKey': environ.get('TMTX_DOMAINKEY'),
            'x-system': environ.get('TMTX_SYSTEM'),
            'x-Password': environ.get('TMTX_PASSWORD'),
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
        self.body = {
            'CheckInDate': '01-12-2022',
            'NoOfNights': 5,
            'CountryCode': 'MX',
            'CityId': 424,
            'GuestNationality': 'EC',
            'NoOfRooms': 1,
            'RoomGuests': [
                {
                    'NoOfAdults': 2,
                    'NoOfChild': 0
                }
            ]
        }

    def handle(self, *args, **options):
        tokens = []
        try:
            log('Getting Information for City: {}'.format(str(self.body['CityId'])))
            r = requests.post(
                environ.get('TMX_HOST'),
                data=json.dumps(self.body),
                headers=self.headers
            )
            hotels = r.json()['Search']['HotelSearchResult']['HotelResults']
            log('Hotels received: {}'.format(len(hotels)))
            for h in hotels:
                tokens.append(h['ResultToken'])
            pool = ThreadPool(processes=len(tokens))
            results = pool.map_async(save_data, tokens)
            pool.close()
            hotels_objects = pool.join()
            print(hotels_objects)
            Hotel.objects.bulk_create(hotels_objects)
            log('Finish')
        except requests.exceptions.RequestException as e:
            log('Unable to get data from the API: {}'.format(e))
        except KeyError as e:
            log(e)

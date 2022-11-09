from os import environ

import json

import requests

from django.core.management.base import BaseCommand, CommandError

from catalogue.models import Item

from task.logging import log


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
            "CheckInDate": "01-12-2022",
            "NoOfNights": 5,
            "CountryCode": "MX",
            "CityId": 424,
            "GuestNationality": "EC",
            "NoOfRooms": 1,
            "RoomGuests": [
                {
                    "NoOfAdults": 2,
                    "NoOfChild": 0
                }
            ]
        }

    def handle(self, *args, **options):
        try:
            log('Getting Hotels Information')
            r = requests.post(
                environ.get('TMX_HOST'),
                data=json.dumps(self.body),
                headers=self.headers
            )
            log('Hotels Received: {}'.format(
                len(r.json()['Search']['HotelSearchResult']['HotelResults']))
            )
        except requests.exceptions.RequestException as e:
            log('Unable to get data from the API: {}'.format(e))
        except KeyError as e:
            log(e)

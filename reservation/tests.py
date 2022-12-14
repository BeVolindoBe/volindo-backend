from time import sleep

from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from common.testing import FIXTURES, get_token

from payment.models import Payment

from reservation.models import Reservation, Room, Guest


class ReservationTestCase(TestCase):

    client = Client()

    fixtures = FIXTURES

    def create_traveler(self, token):
        data = {
            'first_name': 'Eren',
            'last_name': 'Jaeger',
            'email': 'rogney@volindo.com',
            'birth_date': '1900-01-01',
            'phone_country_code': '+52', # +52 Mexico
            'phone_number': '5544332211',
            'title': 'MR',
            'address': 'Mexico Street 10',
            'country': '3fe45243-96b9-4427-89ff-baad6cd696bb', # Mexico
            'city': 'Mexico City',
            'state_province': 'Mexico City',
            'zip_code' : '02000',
            'traveler_status_id':'564c239f-678b-4e5b-a502-969ecdfc23c9'
        }
        response = self.client.post(
            '/agent/travelers/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data=data,
            content_type='application/json'
        )
        return response.json()

    def get_prebook_details(self, token):
        data = {
            'destination': '224d3796-70b6-4d36-942d-e3ce90f97ff9',
            'check_in': '2023-01-01',
            'check_out': '2023-01-05',
            'rooms': [
                {
                    'number_of_adults': 1,
                    'children_age': []
                },
                {
                    'number_of_adults': 1,
                    'children_age': []
                }
            ],
            'currency': 'USD',
            'nationality': 'MX'
        }
        response = self.client.post(
            f'/search/hotels/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data=data,
            content_type='application/json'
        )
        results_id = response.json()['results_id']
        while True:
            response = self.client.get(
                f'/search/hotels/results/{results_id}/',
                HTTP_AUTHORIZATION=f'Bearer {token}'
            )
            if response.json()['status'] != 'pending':
                break
            sleep(1)
        hotel_id = response.json()['hotels'][0]['id']
        response = self.client.get(
            f'/hotels/{hotel_id}/?results_id={results_id}',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        response = self.client.post(
            f'/hotels/rooms/prebook/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data={
                'booking_code': response.json()['rooms'][0]['booking_code'],
                'results_id': response.json()['results_id']
            }
        )
        data = response.json()
        data.update({'results_id': results_id, 'hotel_id': hotel_id})
        return data

    def test_new_reservation(self):
        token = get_token()
        traveler = self.create_traveler(token)
        prebook = self.get_prebook_details(token)
        data = {
            'rooms': [
                {
                    'guests': [
                        {
                            'traveler_id': traveler['id'],
                            'is_lead': True
                        }
                    ],
                    'name': 'Palace Room',
                    'supplements': [
                        {
                            'type': 'At property',
                            'price': '30 AED',
                            'description': 'Mandatory tax'
                        }
                    ]
                },
                {
                    'guests': [
                        {
                            'traveler_id': traveler['id'],
                            'is_lead': True
                        }
                    ],
                    'name': 'Palace Room',
                    'supplements': [
                        {
                            'type': 'At property',
                            'price': '30 AED',
                            'description': 'Mandatory tax'
                        }
                    ]
                }
            ],
            'payment': {
                'commission': '10.50',
                'subtotal': '10.50',
                'total': '10.50',
                'link': True
            },
            'hotel_id': prebook['hotel_id'],
            'results_id': prebook['results_id'],
            'booking_code': prebook['rooms']['booking_code'],
            'policies': {
                'cancellation_policies': [
                    {
                        'from_date': '2022-12-22',
                        'charge': 100.0
                    }
                ],
                'policies': [
                    'No cats',
                    'No smoking'
                ]
            },
            'policies_acceptance': True
        }
        response = self.client.post(
            '/agent/reservations/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, Payment.objects.all().count())
        self.assertEqual(1, Reservation.objects.all().count())
        self.assertEqual(2, Room.objects.all().count())
        self.assertEqual(2, Guest.objects.all().count())

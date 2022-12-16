from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from agent.tests import get_token


class ReservationTestCase(TestCase):

    client = Client()

    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/agent_subscriptions.yaml',
        'catalogue/fixtures/traveler_status.yaml',
        'catalogue/fixtures/countries.yaml',
        'catalogue/fixtures/api_providers.yaml',
        'catalogue/fixtures/destinations.yaml',
        'hotel/fixtures/hotels.yaml',
        'hotel/fixtures/hotel_amenities.yaml',
        'hotel/fixtures/hotel_pictures.yaml',
    ]

    def create_traveler(self, token):
        data = {
            'first_name': 'Eren',
            'last_name': 'Jaeger',
            'email': 'mail@mail.com',
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

    def test_new_reservation(self):
        token = get_token()
        traveler = self.create_traveler(token)
        data = {
            'rooms': [
                {
                'guests': [
                    {
                        'traveler_id': traveler['id'],
                        'is_lead': True
                    }
                ],
                'name': 'Palace Room'
                }
            ],
            'payment': {
                'commission': '10.50',
                'subtotal': '10.50',
                'total': '10.50'
            },
            'hotel_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
            'results_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6'
        }
        response = self.client.post(
            '/agent/reservations/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data=data,
            content_type='application/json'
        )
        print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

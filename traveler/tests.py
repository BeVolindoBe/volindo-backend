from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from common.testing import FIXTURES, get_token


class TravelerTestCase(TestCase):

    client = Client()
    fixtures = FIXTURES

    def test_traveler(self):
        token = get_token()
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
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        traveler_id = response.json()['id']
        response = self.client.get(
            '/agent/travelers/{}/'.format(traveler_id),
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

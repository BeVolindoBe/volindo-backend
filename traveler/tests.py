from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from agent.tests import get_token


class TravelerTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/agent_subscriptions.yaml',
        'catalogue/fixtures/countries.yaml',
        'catalogue/fixtures/phone_country_codes.yaml',
        'catalogue/fixtures/traveler_status.yaml',
    ]

    def test_traveler(self):
        token = get_token()
        data = {
            'first_name': 'Eren',
            'last_name': 'Jaeger',
            'email': 'mail@mail.com',
            'birthdate': '1900-01-01',
            'age': '122',
            'phone_country_code': '3c9efa4d-1b46-4e7c-b042-86f512f6dc8d', # +52 Mexico
            'phone_number': '5544332211',
            'title': 'MR',
            'address': 'Mexico Street 10',
            'country': '47921c88-71ad-11ed-8eed-6ef05e004391', # Mexico
            'city': 'Mexico City',
            'state_province': 'Mexico City',
            'zip_code' : '02000',
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
        print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

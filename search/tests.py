from json import dumps

from django.test import TestCase, Client
from django.core.cache import cache

from rest_framework import status

from agent.tests import get_token


class SearchTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/agent_subscriptions.yaml',
        'catalogue/fixtures/countries.yaml',
        'catalogue/fixtures/api_providers.yaml',
        'catalogue/fixtures/destinations.yaml',
        'hotel/fixtures/hotels.yaml',
        'hotel/fixtures/hotel_amenities.yaml',
        'hotel/fixtures/hotel_pictures.yaml',
    ]

    def test_search(self):
        token = get_token()
        data = {
            "destination": "28e6f8d5-a361-4468-b13e-77ba8ff73ebe",
            "check_in": "2023-01-01",
            "check_out": "2023-01-05",
            "rooms": [
                {
                    "number_of_adults": 1,
                    "children_age": [
                        1
                    ]
                }
            ],
            "currency": "USD",
            "nationality": "MX"
        }
        response = self.client.post(
            f'/search/hotels/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data=data,
            content_type='application/json'
        )
        # print(dumps(responsse.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results_id = response.json()['id']
        response = self.client.get(
            f'/search/hotels/results/{results_id}/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

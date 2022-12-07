from json import dumps

from django.test import TestCase, Client

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
        'catalogue/fixtures/test_cities.yaml',
        'hotel/fixtures/test_hotels.yaml',
        'hotel/fixtures/test_amenities.yaml',
        'hotel/fixtures/test_pictures.yaml',
    ]

    def test_search(self):
        token = get_token()
        data = {
            "destination": "029fecd4-75b0-11ed-ac1d-6ef05e004391",
            "check_in": "2022-12-12",
            "check_out": "2022-12-13",
            "rooms": [
                {
                    "number_of_adults": 2,
                    "childrens_ages": [
                        12
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
        print(dumps(response.json(), indent=4))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # results_id = response.json()['results_id']
        # response = self.client.get(
        #     f'/search/hotels/results/{results_id}/',
        #     HTTP_AUTHORIZATION=f'Bearer {token}'
        # )
        # print(dumps(response.json(), indent=4))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

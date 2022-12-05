from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from agent.tests import get_token


class SearchTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/agent_subscriptions.yaml'
    ]

    def test_search(self):
        token = get_token()
        data = {
            "destination": "018f0c46-27fc-4dd0-9c4c-06d3e368e69d",
            "check_in": "2022-12-12",
            "check_out": "2022-12-12",
            "rooms": [
                {
                    "number_of_adults": 2,
                    "children": [
                        {
                        "age": 12
                        }
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # results_id = response.json()['results_id']
        # response = self.client.get(
        #     f'/search/hotels/results/{results_id}/',
        #     HTTP_AUTHORIZATION=f'Bearer {token}'
        # )
        # print(dumps(response.json(), indent=4))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

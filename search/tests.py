import time

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
        'catalogue/fixtures/destinations.yaml',
        'hotel/fixtures/hotels.yaml',
        'hotel/fixtures/hotel_amenities.yaml',
        'hotel/fixtures/hotel_pictures.yaml',
    ]

    def test_search(self):
        token = get_token()
        data = {
            'destination': '224d3796-70b6-4d36-942d-e3ce90f97ff9',
            'check_in': '2023-01-01',
            'check_out': '2023-01-05',
            'rooms': [
                {
                    'number_of_adults': 1,
                    'children_age': [
                        1
                    ]
                },
                {
                    'number_of_adults': 1,
                    'children_age': [
                        1
                    ]
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
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results_id = response.json()['results_id']
        while True:
            response = self.client.get(
                f'/search/hotels/results/{results_id}/',
                HTTP_AUTHORIZATION=f'Bearer {token}'
            )
            # print(response.json())
            if response.json()['status'] != 'pending':
                break
            time.sleep(1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        hotel_id = response.json()['hotels'][0]['id']
        response = self.client.get(
            f'/hotels/{hotel_id}/?results_id={results_id}',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(dumps(response.json(), indent=4))
        response = self.client.post(
            f'/hotels/rooms/prebook/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data={
                'booking_code': response.json()['rooms'][0]['booking_code'],
                'results_id': response.json()['results_id']
            }
        )
        print(print(dumps(response.json(), indent=4)))

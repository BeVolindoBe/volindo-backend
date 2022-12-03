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

    query_params = '?destination=mx&check_in=2023-01-10&check_out=2023-01-14&nationality=MX&adults=2&children=1'

    def test_notifications(self):
        token = get_token()
        response = self.client.get(
            f'/search/hotels/{self.query_params}',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results_id = response.json()['results_id']
        response = self.client.get(
            f'/search/hotels/results/{results_id}/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

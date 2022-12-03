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

    def test_notifications(self):
        token = get_token()
        response = self.client.get(
            '/search/hotels/?destination=mx',
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

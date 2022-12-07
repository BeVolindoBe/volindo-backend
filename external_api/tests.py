from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from agent.tests import get_token

from hotel.models import HotelPicture, Hotel


class StaticTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/agent_subscriptions.yaml',
        'catalogue/fixtures/api_providers.yaml'
    ]

    def test_search(self):
        token = get_token()
        response = self.client.get(
            f'/external-api/static/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from json import dumps

from django.test import TestCase, Client
from django.contrib.auth.models import User

from rest_framework import status

from account.tests import get_token

from agent.models import Agent


class AgentTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/agent_subscriptions.yaml',
    ]

    def test_get_agent_by_id(self):
        token = get_token()
        response = self.client.get('/agents/', HTTP_AUTHORIZATION=f'Bearer {token}')
        print(response)
        print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

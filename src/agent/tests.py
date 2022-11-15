from json import dumps

from django.test import TestCase, Client

from rest_framework import status


class AgentTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/countries.yaml',
        'catalogue/fixtures/phone_country_codes.yaml',
        'agent/fixtures/agents.yaml',
    ]

    def test_get_agent_by_id(self):
        response = self.client.get('/agents/97d7ea3b-99d3-4123-b4a2-8fc38b6a63ff')
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

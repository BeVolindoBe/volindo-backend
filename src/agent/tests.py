from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from agent.models import Agent


class AgentTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/countries.yaml',
        'catalogue/fixtures/phone_country_codes.yaml',
        'agent/fixtures/agents.yaml',
    ]

    def test_new_agent(self):
        data = {
            'first_name': 'Travel',
            'last_name': 'Agent',
            'email': 'user@example.com',
            'gender': 'M',
            'birthdate': '2022-11-15',
            'country': 'f1d1d7a8-bffe-4d2d-81d4-9d47a2b080ce',
            'phone_contry_code': '3c9efa4d-1b46-4e7c-b042-86f512f6dc8d',
            'web_site': 'https://example.com'
        }
        response = self.client.post('/agents/', data=data)
        # print(dumps(response.json(), indent=4))
        self.assertEqual(2, Agent.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_agent_by_id(self):
        response = self.client.get('/agents/97d7ea3b-99d3-4123-b4a2-8fc38b6a63ff/')
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

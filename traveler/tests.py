from json import dumps

from django.test import TestCase, Client

from rest_framework import status


class TravelerTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/countries.yaml',
        'catalogue/fixtures/phone_country_codes.yaml',
        'catalogue/fixtures/traveler_status.yaml',
        'account/fixtures/users.yaml',
        'agent/fixtures/agents.yaml',
        'traveler/fixtures/travelers.yaml'
    ]
    agent_id = '97d7ea3b-99d3-4123-b4a2-8fc38b6a63ff'
    traveler_id = '26558871-d77f-4ee4-8f3f-f8a7cefd84a5'

    def test_get_traveler_by_id(self):
        response = self.client.get('/users/{}/travelers/{}/'.format(self.agent_id, self.traveler_id))
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

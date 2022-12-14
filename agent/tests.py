from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from account.tests import get_token


class AgentTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/countries.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/agent_subscriptions.yaml',
    ]

    def test_get_agent_detail(self):
        token = get_token()
        response = self.client.get('/agent/', HTTP_AUTHORIZATION=f'Bearer {token}')
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_agent(self):
        token = get_token()
        data = {
            'first_name': 'Jhon',
            'last_name': 'Doe'
        }
        response = self.client.patch(
            '/agent/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], 'Jhon')
        self.assertEqual(response.json()['last_name'], 'Doe')
    
    def test_update_agent_foreign_keys(self):
        token = get_token()
        data = {
            'country': '7924d644-73cb-4beb-871f-33534f05e287',
        }
        response = self.client.patch(
            '/agent/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data=data,
            content_type='application/json'
        )
        print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['country']['description'], 'United States')
    
    def test_update_agent_foreign_keys_read_only(self):
        token = get_token()
        data = {
            'agent_status': '850e92dd-a12d-4c58-94ef-782ec4c4edc7',
            'last_name': 'Not updated',
            'agent_subscription': '6e652935-cd9f-4b66-846b-fc1da9315b98'
        }
        response = self.client.patch(
            '/agent/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

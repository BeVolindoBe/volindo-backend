from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from common.testing import FIXTURES, USER_ID

from user.models import User

from agent.models import Agent


class AgentTestCase(TestCase):

    client = Client()
    fixtures = FIXTURES

    def test_get_agent_detail(self):
        user_id = str(User.objects.first().id)
        response = self.client.get(
            f'/users/{USER_ID}/',
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_agent(self):
        data = {
            'city': 'Azcapotzalco',
            'zip_code': '02000'
        }
        response = self.client.patch(
            f'/users/{USER_ID}/',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['city'], 'Azcapotzalco')
        self.assertEqual(response.json()['zip_code'], '02000')
    
    def test_update_agent_foreign_keys(self):
        data = {
            'country': '7f494634-379c-4c3a-ad0f-c84db69076ab', # Mexico
        }
        response = self.client.patch(
            f'/users/{USER_ID}/',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['country']['country_name'], 'Mexico')
    
    def test_update_agent_foreign_keys_read_only(self):
        data = {
            'agent_status': '850e92dd-a12d-4c58-94ef-782ec4c4edc7',
            'full_name': 'Not updated',
            'agent_subscription': '6e652935-cd9f-4b66-846b-fc1da9315b98'
        }
        response = self.client.patch(
            f'/users/{USER_ID}/',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(
            response.json()['agent_subscription']['id'],
            '6e652935-cd9f-4b66-846b-fc1da9315b98'
        )

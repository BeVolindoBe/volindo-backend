from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from agent.tests import get_token


class TravelerTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/agent_subscriptions.yaml'
    ]

    def test_notifications(self):
        token = get_token()
        response = self.client.get(
            '/agent/notifications/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification_id = response.json()[0]['id']
        data = {
            'read': True
        }
        response = self.client.patch(
            f'/agent/notifications/{notification_id}/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['read'], True)
        response = self.client.get(
            '/agent/notifications/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

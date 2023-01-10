from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from common.testing import FIXTURES

from user.models import User

from agent.models import Agent


class UserTestCase(TestCase):

    client = Client()
    fixtures = FIXTURES

    def test_new_user(self):
        data = {
            'external_id': 'c0a80101-0000-0000-0000-000000000000',
            'email': 'email@email.com',
            'full_name': 'Eren Jaeger'
        }
        response = self.client.post(
            '/accounts/',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, Agent.objects.all().count()) # 1 from fixtures + 1 from test
    
    def test_duplicate_user(self):
        data = {
            'external_id': 'c0a80101-0000-0000-0000-000000000002',
            'email': 'mail@mail.com',
            'full_name': 'Jaeger Eren'
        }
        response = self.client.post(
            '/accounts/',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_user_detail(self):
        user_id = str(User.objects.all().first().id)
        response = self.client.get(
            f'/accounts/{user_id}/',
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

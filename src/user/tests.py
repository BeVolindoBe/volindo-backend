from json import dumps

from django.test import TestCase, Client

from rest_framework import status


class UserTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/user_status.yaml',
        'user/fixtures/users.yaml'
    ]

    def test_get_user_by_id(self):
        response = self.client.get('/users/759a75bb-26e3-410e-94b5-9138ebc2e47a')
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from json import dumps

from django.test import TestCase, Client
from django.contrib.auth.models import User

from rest_framework import status


class USerTestCase(TestCase):

    client = Client()

    def test_new_user(self):
        self.assertEqual(0, User.objects.all().count())
        data = {
            'first_name': 'Travel',
            'last_name': 'Agent',
            'username': 'user@example.com',
            'email': 'user@example.com',
            'password': 'W1D78#Ae9O5r',
            'password2': 'W1D78#Ae9O5r',
        }
        response = self.client.post('/accounts/register/', data=data)
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, User.objects.all().count())

    def test_get_token(self):
        data = {
            'first_name': 'Travel',
            'last_name': 'Agent',
            'username': 'user@example.com',
            'email': 'user@example.com',
            'password': 'W1D78#Ae9O5r',
            'password2': 'W1D78#Ae9O5r',
        }
        response = self.client.post('/accounts/register/', data=data)
        # print(dumps(response.json(), indent=4))
        response = self.client.post('/accounts/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'username': 'user@example.com',
            'password': 'W1D78#Ae9O5r'
        }
        response = self.client.post('/accounts/login/', json=data)

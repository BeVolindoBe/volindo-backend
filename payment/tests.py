from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from payment.models import Payment, ExternalAgent


class ExternalAgentTestCase(TestCase):

    client = Client()
    def test_new_external_agent(self):
        data = {
            'external_id': 'ABCDE',
            'agent_name': 'Jhon Doe',
            'phone_number': '5521314151',
            'image': 'https://example.com',
            'agent_email': 'jhon@doe.com'
        }
        response = self.client.post('/payments/external_agents/', data=data)
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, ExternalAgent.objects.all().count())
        self.assertEqual(1, Payment.objects.all().count())
        response = self.client.post('/payments/external_agents/', data=data)
        # print(dumps(response_2.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, ExternalAgent.objects.all().count())
        self.assertEqual(2, Payment.objects.all().count())

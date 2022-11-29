from json import dumps

from django.test import TestCase, Client

from rest_framework import status


class BankAccountTestCase(TestCase):

    client = Client()

    fixtures = [
        'bank/fixtures/banks.yaml',
    ]

    def test_get_bank_accounts_list(self):
        response = self.client.get('/bank-accounts/')
        print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

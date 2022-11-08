from json import dumps

from django.test import TestCase, Client

from rest_framework import status


class CatalogTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalog/fixtures/catalogs.yaml',
        'catalog/fixtures/countries.yaml'
    ]

    def test_get_all_catalogs(self):
        response = self.client.get('catalogs/all/')
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

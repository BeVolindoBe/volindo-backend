from json import dumps

from django.test import TestCase, Client

from common.testing import FIXTURES, get_token

from rest_framework import status


class CatalogueTestCase(TestCase):

    client = Client()
    fixtures = FIXTURES

    def test_get_all_catalogues(self):
        token = get_token()
        response = self.client.get(
            '/catalogues/all/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_catalogue_by_slug(self):
        token = get_token()
        response = self.client.get(
            '/catalogues/countries/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )           
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destinations_autocmomplete(self):
        token = get_token()
        response = self.client.get(
            '/catalogues/destinations/?destination=Victori',
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )           
        print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

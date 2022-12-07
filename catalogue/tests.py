from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from account.tests import get_token


class CatalogueTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/amenities.yaml',
        'catalogue/fixtures/countries.yaml',
        'catalogue/fixtures/test_cities.yaml',
    ]

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
            '/catalogues/cities/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )           
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destinations_autocmomplete(self):
        token = get_token()
        response = self.client.get(
            '/catalogues/destinations/?destination=chakc',
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )           
        print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

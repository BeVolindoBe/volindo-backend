from json import dumps

from django.test import TestCase, Client

from rest_framework import status


class CatalogueTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml'
    ]

    def test_get_all_catalogues(self):
        response = self.client.get('/catalogues/all')
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_catalogue_by_slug(self):
        response = self.client.get('/catalogues/agent_status')
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

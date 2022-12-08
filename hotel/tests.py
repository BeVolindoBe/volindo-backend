from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from agent.tests import get_token


class HotelTestCase(TestCase):

    client = Client()
    hotel_id = '8ef1885f-e24b-4183-bcb2-67d44c5d448f'

    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/agent_subscriptions.yaml',
        'catalogue/fixtures/countries.yaml',
        'catalogue/fixtures/api_providers.yaml',
        'catalogue/fixtures/destinations.yaml',
        'hotel/fixtures/hotels.yaml',
        'hotel/fixtures/hotel_amenities.yaml',
        'hotel/fixtures/hotel_pictures.yaml',
    ]

    def test_update_traveler_by_id(self):
        token = get_token()
        response = self.client.get(
            '/hotels/{}/'.format(self.hotel_id),
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

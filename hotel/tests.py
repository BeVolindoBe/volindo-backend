from json import dumps

from django.test import TestCase, Client

from rest_framework import status


class HotelTestCase(TestCase):

    client = Client()
    hotel_id = '38a11835-14f1-4a5c-9e46-77d1990db1d8'

    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/countries.yaml',
        'catalogue/fixtures/destinations.yaml',
        'catalogue/fixtures/phone_country_codes.yaml',
        'catalogue/fixtures/amenities.yaml',
        'account/fixtures/users.yaml',
        'agent/fixtures/agents.yaml',
        'hotel/fixtures/hotels_test.yaml',
        'hotel/fixtures/hotels_pictures_test.yaml',
        'hotel/fixtures/hotels_amenities_test.yaml',
    ]

    def test_update_traveler_by_id(self):
        response = self.client.get('/hotels/{}/'.format(self.hotel_id))
        print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

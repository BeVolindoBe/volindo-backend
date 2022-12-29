import time

from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from common.testing import FIXTURES, get_token


class SearchTestCase(TestCase):

    client = Client()
    fixtures = FIXTURES

    # def test_search_hotels(self):
    #     token = get_token()
    #     data = {
    #         'destination': '224d3796-70b6-4d36-942d-e3ce90f97ff9',
    #         'check_in': '2023-01-05',
    #         'check_out': '2023-01-09',
    #         'rooms': [
    #             {
    #                 'number_of_adults': 1,
    #                 'children_age': []
    #             }
    #         ],
    #         'currency': 'USD',
    #         'nationality': 'MX'
    #     }
    #     response = self.client.post(
    #         f'/search/hotels/',
    #         HTTP_AUTHORIZATION=f'Bearer {token}',
    #         data=data,
    #         content_type='application/json'
    #     )
    #     # print(dumps(response.json(), indent=4))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     results_id = response.json()['results_id']
    #     while True:
    #         response = self.client.get(
    #             f'/search/hotels/results/{results_id}/',
    #             HTTP_AUTHORIZATION=f'Bearer {token}'
    #         )
    #         if response.json()['status'] != 'pending':
    #             break
    #         time.sleep(2)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     hotel_id = response.json()['hotels'][0]['id']
    #     print('Hotels', len(response.json()['hotels']))
    #     response = self.client.get(
    #         f'/hotels/{hotel_id}/?results_id={results_id}',
    #         HTTP_AUTHORIZATION=f'Bearer {token}'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # print(dumps(response.json(), indent=4))
    #     response = self.client.post(
    #         f'/hotels/rooms/prebook/',
    #         HTTP_AUTHORIZATION=f'Bearer {token}',
    #         data={
    #             'booking_code': response.json()['rooms'][0]['booking_code'],
    #             'results_id': response.json()['results_id']
    #         }
    #     )
    #     # print(dumps(response.json(), indent=4))

    def test_search_return_flights(self):
        token = get_token()
        data = {
            'adults': 1,
            'children': 0,
            'infants': 0,
            'flight_type': 'return',
            'flight_class': 'economy',
            'departure_date': '2023-01-10',
            'return_date': '2023-01-15',
            'origin': 'BLR',
            'destination': 'MAA',
        }
        response = self.client.post(
            f'/search/flights/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        counter = 0
        while True:
            results_id = response.json()['results_id']
            response = self.client.get(
                f'/search/flights/results/{results_id}/',
                HTTP_AUTHORIZATION=f'Bearer {token}'
            )
            if response.json()['status'] != 'pending':
                print(dumps(response.json(), indent=4))
                break
            time.sleep(5)
            counter += 1
            if counter > 20:
                self.assertEqual(0, 1)
                break

    def test_search_single_flights(self):
        token = get_token()
        data = {
            'adults': 1,
            'children': 0,
            'infants': 0,
            'flight_type': 'one_way',
            'flight_class': 'economy',
            'departure_date': '2023-01-10',
            'return_date': '',
            'origin': 'BLR',
            'destination': 'MAA',
        }
        response = self.client.post(
            f'/search/flights/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        counter = 0
        while True:
            results_id = response.json()['results_id']
            response = self.client.get(
                f'/search/flights/results/{results_id}/',
                HTTP_AUTHORIZATION=f'Bearer {token}'
            )
            if response.json()['status'] != 'pending':
                # print(dumps(response.json(), indent=4))s
                break
            time.sleep(5)
            counter += 1
            if counter > 20:
                self.assertEqual(0, 1)
                break

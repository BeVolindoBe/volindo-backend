from time import sleep

from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from common.testing import FIXTURES, USER_ID


class SubscriptionPayment(TestCase):

    client = Client()
    fixtures = FIXTURES

    def test_get_stripe_session(self):
        response = self.client.get(
            f'/users/{USER_ID}/payments/create-session/',
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)


# class PaymentReservationTestCase(TestCase):

#     client = Client()
#     fixtures = FIXTURES

#     def create_traveler(self, token):
#         data = {
#             'first_name': 'Eren',
#             'last_name': 'Jaeger',
#             'email': 'mail@mail.com',
#             'birth_date': '1900-01-01',
#             'phone_country_code': '+52', # +52 Mexico
#             'phone_number': '5544332211',
#             'title': 'MR',
#             'address': 'Mexico Street 10',
#             'country': '87ddfd52-d402-4867-8e44-1e57b3a6f772', # United Arab Emirates
#             'city': 'Mexico City',
#             'state_province': 'Mexico City',
#             'zip_code' : '02000',
#             'traveler_status_id':'564c239f-678b-4e5b-a502-969ecdfc23c9'
#         }
#         response = self.client.post(
#             '/agent/travelers/',
#             HTTP_AUTHORIZATION=f'Bearer {token}',
#             data=data,
#             content_type='application/json'
#         )
#         return response.json()

#     def get_prebook_details(self, token):
#         data = {
#             'destination': '224d3796-70b6-4d36-942d-e3ce90f97ff9',
#             'check_in': '2023-01-01',
#             'check_out': '2023-01-05',
#             'rooms': [
#                 {
#                     'number_of_adults': 1,
#                     'children_age': []
#                 },
#                 {
#                     'number_of_adults': 1,
#                     'children_age': []
#                 }
#             ],
#             'currency': 'USD',
#             'nationality': 'MX'
#         }
#         response = self.client.post(
#             f'/search/hotels/',
#             HTTP_AUTHORIZATION=f'Bearer {token}',
#             data=data,
#             content_type='application/json'
#         )
#         results_id = response.json()['results_id']
#         while True:
#             response = self.client.get(
#                 f'/search/hotels/results/{results_id}/',
#                 HTTP_AUTHORIZATION=f'Bearer {token}'
#             )
#             if response.json()['status'] != 'pending':
#                 break
#             sleep(1)
#         hotel_id = response.json()['hotels'][0]['id']
#         response = self.client.get(
#             f'/hotels/{hotel_id}/?results_id={results_id}',
#             HTTP_AUTHORIZATION=f'Bearer {token}'
#         )
#         response = self.client.post(
#             f'/hotels/rooms/prebook/',
#             HTTP_AUTHORIZATION=f'Bearer {token}',
#             data={
#                 'booking_code': response.json()['rooms'][0]['booking_code'],
#                 'results_id': response.json()['results_id']
#             }
#         )
#         data = response.json()
#         data.update({'results_id': results_id, 'hotel_id': hotel_id})
#         return data

#     def get_payment_id(self):
#         token = get_token()
#         traveler = self.create_traveler(token)
#         prebook = self.get_prebook_details(token)
#         data = {
#             'rooms': [
#                 {
#                     'guests': [
#                         {
#                             'traveler_id': traveler['id'],
#                             'is_lead': True
#                         }
#                     ],
#                     'name': 'Palace Room',
#                     'supplements': [
#                         {
#                             'type': 'At property',
#                             'price': '30 AED',
#                             'description': 'Mandatory tax'
#                         }
#                     ]
#                 },
#                 {
#                     'guests': [
#                         {
#                             'traveler_id': traveler['id'],
#                             'is_lead': True
#                         }
#                     ],
#                     'name': 'Palace Room',
#                     'supplements': [
#                         {
#                             'type': 'At property',
#                             'price': '30 AED',
#                             'description': 'Mandatory tax'
#                         }
#                     ]
#                 }
#             ],
#             'payment': {
#                 'commission': '10.50',
#                 'subtotal': '10.50',
#                 'total': '10.50',
#                 'link': True
#             },
#             'hotel_id': prebook['hotel_id'],
#             'results_id': prebook['results_id'],
#             'booking_code': prebook['rooms']['booking_code'],
#             'policies': {
#                 'cancellation_policies': [
#                     {
#                         'from_date': '2022-12-22',
#                         'charge': 100.0
#                     }
#                 ],
#                 'policies': [
#                     'No cats',
#                     'No smoking'
#                 ]
#             },
#             'policies_acceptance': True
#         }
#         response = self.client.post(
#             '/agent/reservations/',
#             HTTP_AUTHORIZATION=f'Bearer {token}',
#             data=data,
#             content_type='application/json'
#         )
#         return response.json()

#     # def test_get_agent_payments(self):
#     #     token = get_token()
#     #     self.get_payment_id()
#     #     response = self.client.get(
#     #         '/agent/payments/',
#     #         HTTP_AUTHORIZATION=f'Bearer {token}',
#     #         content_type='application/json'
#     #     )
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)

#     # def test_get_payment_detail(self):
#     #     token = get_token()
#     #     payment_id = self.get_payment_id()['id']
#     #     response = self.client.get(
#     #         f'/agent/payments/{payment_id}/',
#     #         HTTP_AUTHORIZATION=f'Bearer {token}',
#     #         content_type='application/json'
#     #     )
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     print(dumps(response.json(), indent=4))

#     def test_pay_reservation(self):
#         token = get_token()
#         payment = self.get_payment_id()
#         card_data = {
#             'card_number': '4242424242424242',
#             'cvv': '123',
#             'exp_date': '01/2025',
#             'card_name': 'Jhon Doe'
#         }
#         response = self.client.post(
#             f'/agent/payments/{payment["id"]}/reservation/',
#             HTTP_AUTHORIZATION=f'Bearer {token}',
#             content_type='application/json',
#             data=card_data,
#         )
#         response = self.client.get(
#             f'/agent/reservations/',
#             HTTP_AUTHORIZATION=f'Bearer {token}',
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         print(dumps(response.json(), indent=4))
#         # while True:
#         #     print('Waiting for status update')
#         #     response = self.client.get(
#         #     f'/agent/reservations/',
#         #         HTTP_AUTHORIZATION=f'Bearer {token}',
#         #         content_type='application/json'
#         #     )
#         #     if response.json()['status'] != 'pending':
#         #         break
#         #     sleep(10)

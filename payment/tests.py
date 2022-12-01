from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from agent.models import Agent

from payment.models import ReservationPayment, Room, Guest


class ReservationPaymentTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/agent_subscriptions.yaml',
        'catalogue/fixtures/traveler_status.yaml'
    ]

    def test_new_reservation_payment(self):
        data = {
            'agent': {
                'first_name': 'Eren',
                'last_name': 'Jaeger',
                'email': 'juanpablo@volindo.com',
                'phone_number': '5566778899',
                'photo': 'https://example.com'
            },
            'hotels': [
                {
                    'hotel_name': 'Hotel',
                    'check_in': '2022-11-29',
                    'check_out': '2022-11-29',
                    'rooms': [
                        {
                            'description': 'Room 1',
                            'guests': [
                                {
                                    'first_name': 'Jhon',
                                    'last_name': 'Doe',
                                    'email': 'juanpablo@volindo.com',
                                    'age': 22,
                                    'phone_number': '5544332211',
                                    'title': 'MR'
                                }
                            ]
                        }
                    ]
                }
            ],
            'amount': '100.00',
            'commission': '5.00',
            'total': '105.00'
        }
        response = self.client.post(
            '/payments/reservations/',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(1, Agent.objects.all().count())
        response = self.client.post(
            '/payments/reservations/',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(1, Agent.objects.all().count())
        self.assertEqual(2, ReservationPayment.objects.all().count())
        self.assertEqual(2, Guest.objects.all().count())
        self.assertEqual(2, Room.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payment_id = response.json()['payment_id']
        response = self.client.get(
            '/payments/{}/'.format(payment_id),
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card_data = {
            'card_number': '4242424242424242',
            'cvv': '123',
            'exp_date': '01/2025',
            'card_name': 'Jhon Doe'
        }
        response = self.client.post(
            '/payments/{}/'.format(payment_id),
            data=card_data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(
            ReservationPayment.objects.get(id=payment_id).approved_at,
            None
        )

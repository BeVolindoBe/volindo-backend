from json import dumps

from django.test import TestCase, Client

from rest_framework import status

from agent.models import Agent

from traveler.models import Traveler

from payment.models import ReservationPayment


class ReservationPaymentTestCase(TestCase):

    client = Client()
    fixtures = [
        'catalogue/fixtures/catalogues.yaml',
        'catalogue/fixtures/agent_status.yaml',
        'catalogue/fixtures/traveler_status.yaml'
    ]

    def test_new_reservation_payment(self):
        data = {
            'agent': {
                'first_name': 'Jhon',
                'last_name': 'Doe',
                'email': 'user@example.com',
                'phone_number': '5566778899'
            },
            'amount': '100.50',
            'commission': '5.45',
            'total': '106.00',
            'hotels': [
                {
                    'hotel_name': 'Hotel',
                    'check_in': '2022-11-30',
                    'check_out': '2022-12-10',
                    'room_description': 'Room 1',
                    'guests': [
                        {
                            'first_name': 'Eren',
                            'last_name': 'Jaeger',
                            'email': 'user@example.com',
                            'age': 22,
                            'phone_number': '5500998877',
                            'title': 'ms'
                        }
                    ]
                }
            ]
        }
        response = self.client.post(
            '/payments/reservations/',
            data=data,
            content_type='application/json'
        )
        response = self.client.post(
            '/payments/reservations/',
            data=data,
            content_type='application/json'
        )
        # print(dumps(response.json(), indent=4))
        self.assertEqual(1, Agent.objects.all().count())
        self.assertEqual(1, ReservationPayment.objects.all().count())
        self.assertEqual(1, Traveler.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payment_id = response.json()['payment_id']
        card_data = {
            'card_number': '4242424242424242',
            'cvv': '123',
            'exp_date': '11/2022',
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

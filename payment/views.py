from os import environ

from uuid import uuid4

from datetime import datetime

from decimal import Decimal

import requests

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from agent.models import Agent

from traveler.models import Traveler

from payment.models import ReservationPayment, Reservation
from payment.serializers import ReservationPaymentSerializer, CardSerializer


class ResponseData:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data


headers = {
    'Authorization': f'Bearer {environ["PAYMENT_AUTH"]}',
    'Content-Type': 'application/x-www-form-urlencoded',
}


class PaymentView(APIView):

    def validate_card(self, data):
        exp_date = data['exp_date'].value
        url = environ['PAYMENT_TOKEN']
        payload = 'card%5Bnumber%5D={}&card%5Bexp_month%5D={}&card%5Bexp_year%5D={}&card%5Bcvc%5D={}'.format(
            data['card_number'].value,
            exp_date.split('/')[0],
            exp_date.split('/')[1],
            data['cvv'].value,
        )
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            return ResponseData(200, 'Success', response.json())
        else:
            return ResponseData(400, response.json()['error']['message'], None)

    def execute_payment(self, total, token):
            amount = str(int(total)) + '00'
            url = environ['PAYMENT_URL']
            payload = 'amount={}&currency={}&source={}&description=Volindo%20Book'.format(
                int(amount), environ['DEFAULT_CURRENCY'], token
            )
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                return ResponseData(200, 'Payment approved.', None)
            else:
                return ResponseData(400, response.json()['error']['message'], None)

    @swagger_auto_schema(request_body=CardSerializer)
    def post(self, request, payment_id):
        data = CardSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            rp = ReservationPayment.objects.get(id=payment_id)
            token = self.validate_card(data) # validate card and obtain token
            if token.status == 200:
                payment = self.execute_payment(rp.total, token.data['id']) # execute payment process
                if payment.status == 200:
                    rp.approved_at = datetime.now()
                    rp.save()
                    return Response(
                        {'message': payment.message}, 
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {'message': payment.message},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'message': token.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'message': 'Invalid credit card information'},
            status=status.HTTP_400_BAD_REQUEST
        )


class NewReservationPayment(APIView):

    def create_user(self, data):
        user, created = User.objects.get_or_create(
            username=data['email'].value,
            email=data['email'].value,
            first_name=data['first_name'].value,
            last_name=data['last_name'].value
        )
        user.set_password(str(uuid4()))
        user.save()
        return user

    def create_agent(self, user, data):
        agent, created = Agent.objects.get_or_create(
            user=user,
            first_name=data['first_name'].value,
            last_name=data['last_name'].value,
            email=data['email'].value,
        )
        return agent

    def create_payment(self, agent, data):
        payment, created = ReservationPayment.objects.get_or_create(
            agent=agent,
            amount=Decimal(data['amount'].value),
            commission=Decimal(data['commission'].value),
            total=Decimal(data['total'].value),
        )
        return payment, created

    def create_traveler(self, agent, data):
        Traveler.objects.bulk_create(
            [Traveler(
                agent=agent,
                first_name=t['first_name'],
                last_name=t['last_name'],
                email=t['email'],
                age=t['age'],
                phone_number=t['phone_number'],
            ) for t in data]
        )

    def create_reservations(self, agent, payment, created, data):
        if created:
            reservations = []
            for r in data.value:
                reservations.append(
                    Reservation(
                        payment=payment,
                        hotel_name=r['hotel_name'],
                        check_in=r['check_in'],
                        check_out=r['check_out']
                    )
                )
                self.create_traveler(agent, r['guests'])
            Reservation.objects.bulk_create(reservations)

    @swagger_auto_schema(request_body=ReservationPaymentSerializer)
    def post(self, request):
        data = ReservationPaymentSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            user = self.create_user(data['agent'])
            agent = self.create_agent(user, data['agent'])
            payment, created = self.create_payment(agent, data)
            self.create_reservations(agent, payment, created, data['hotels'])
            return Response(
                {'message': 'Payment created.', 'payment_id': str(payment.id)},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'Bad request.'},
            status=status.HTTP_400_BAD_REQUEST
        )

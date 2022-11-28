from uuid import uuid4

from decimal import Decimal

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_serializer_method

from agent.models import Agent

from traveler.models import Traveler

from payment.models import ReservationPayment, Reservation
from payment.serializers import ReservationPaymentSerializer


class NewReservationPayment(APIView):

    def create_user(self, data):
        user, created = User.objects.get_or_create(
            username=data['email'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.set_password(str(uuid4()))
        user.save()
        return user

    def create_agent(self, user, data):
        agent, created = Agent.objects.get_or_create(
            user=user,
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
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
                birthdate=t['birthdate'],
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
                        room_description=r['room_description'],
                        check_in=r['check_in'],
                        check_out=r['check_out']
                    )
                )
                self.create_traveler(agent, r['guests'])
            Reservation.objects.bulk_create(reservations)

    @swagger_serializer_method(serializer_or_field=ReservationPaymentSerializer)
    def post(self, request):
        data = ReservationPaymentSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            user = self.create_user(data['agent'])
            agent = self.create_agent(user, data['agent'])
            payment, created = self.create_payment(agent, data)
            self.create_reservations(agent, payment, created, data['hotels'])
            return Response(
                {'message': 'Payment approved.', 'payment_id': str(payment.id)},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'Bad request.'},
            status=status.HTTP_400_BAD_REQUEST
        )

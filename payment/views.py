from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from payment.serializers import ReservationPaymentSerializer
from payment.models import ReservationPayment


class ReservationPayment(CreateAPIView):

    serializer_class = ReservationPaymentSerializer
    queryset = ReservationPayment.objects.all()

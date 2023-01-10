from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utilities.payments import pay_reservation

from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentDetailSerializer, CardSerializer
from payment.connection import get_stripe_session


class PaymentList(ListAPIView):

    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.get(agent__user=self.request.user)


class PaymentDetail(RetrieveAPIView):

    serializer_class = PaymentDetailSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        return Payment.objects.all()


class ReservationPayment(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, pk):
        data = CardSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            card_details = data.data
            payment = pay_reservation(payment_id=pk, card_details=card_details)
            return Response(payment.data, status=payment.status_code)



class PaymentSession(APIView):

    def get(self, request, user__external_id):
        return Response(get_stripe_session(), status=status.HTTP_200_OK)

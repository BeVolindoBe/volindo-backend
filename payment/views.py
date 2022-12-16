from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentDetailSerializer, CardSerializer


class PaymentList(ListAPIView):

    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.get(agent__user=self.request.user)


class PaymentDetail(RetrieveAPIView):

    serializer_class = PaymentDetailSerializer

    def get_queryset(self):
        return Payment.objects.all()


class ReservationPayment(RetrieveAPIView):

    def post(self, request, pk):
        return Response(
            {
                'message': 'OK'
            },
            status=status.HTTP_200_OK
        )

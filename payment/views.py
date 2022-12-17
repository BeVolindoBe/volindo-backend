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


class ReservationPayment(APIView):

    def post(self, request, pk):
        data = CardSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            cleaned_data = data.data
            return Response(cleaned_data, status=status.HTTP_200_OK)

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from utilities.payments import pay_reservation

from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentDetailSerializer, CardSerializer


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

    def post(self, request, pk):
        data = CardSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            card_details = data.data
            payment = pay_reservation(payment_id=pk, card_details=card_details)
            return Response(payment.data, status=payment.status_code)

from rest_framework.generics import ListAPIView, RetrieveAPIView

from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentDetailSerializer


class PaymentList(ListAPIView):

    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.get(agent__user=self.request.user)


class PaymentDetail(RetrieveAPIView):

    serializer_class = PaymentDetailSerializer

    def get_queryset(self):
        return Payment.objects.all()

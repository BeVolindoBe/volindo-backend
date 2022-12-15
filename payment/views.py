from rest_framework.generics import ListAPIView

from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentList(ListAPIView):

    serializer_class = PaymentSerializer

    def get_queryset(self, request):
        return Payment.objects.filter(agent__user=request.user)

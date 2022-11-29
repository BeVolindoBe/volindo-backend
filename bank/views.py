from rest_framework.generics import ListAPIView

from bank.models import BankAccount
from bank.serializers import BanAccountSerializer


class BankList(ListAPIView):

    serializer_class = BanAccountSerializer
    queryset = BankAccount.objects.all()

from rest_framework import serializers

from bank.models import BankAccount


class BanAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = '__all__'

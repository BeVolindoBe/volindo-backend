from datetime import datetime

from rest_framework import serializers

from catalogue.models import Item
from catalogue.serializers import ItemSerializer

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            'id',
            'commission',
            'subtotal',
            'total',
            'approved_at',
            'payment_type',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['payment_type'] = ItemSerializer(
            Item.objects.get(id=instance.payment_type)
        ).data


class CardSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    exp_date = serializers.CharField()
    cvv = serializers.CharField()
    card_name = serializers.CharField()

    def validate(self, attrs):
        if len(attrs['card_number']) != 16:
            raise serializers.ValidationError(
                {'card_number': 'Invalid card number.'}
            )
        try:
            datetime.strptime('{}-{}-1'.format(
                attrs['exp_date'].split('/')[1], # year yyyy
                attrs['exp_date'].split('/')[0], # month mm
            ), '%Y-%m-%d')
        except ValueError:
            raise serializers.ValidationError(
                {'exp_date': 'Invalid expiration date.'}
            )
        try:
            int(attrs['cvv'])
        except ValueError:
            raise serializers.ValidationError(
                {'cvv': 'Invalid CVV.'}
            )
        return attrs

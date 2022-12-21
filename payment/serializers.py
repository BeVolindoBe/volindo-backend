from datetime import datetime

from rest_framework import serializers

from catalogue.serializers import ItemSerializer

from payment.models import Payment

from agent.serializers import AgentSerializer

from reservation.models import Reservation
from reservation.serializers import ReservationModelSerializer

from hotel.serializers import HotelSerializer


class PaymentDetailSerializer(serializers.ModelSerializer):

    agent = AgentSerializer()

    class Meta:
        model = Payment
        fields = (
            'agent',
            'id',
            'commission',
            'subtotal',
            'total',
            'approved_at',
            'payment_type'
        )

    def get_reservation_details(self, payment_id):
        try:
            reservation = Reservation.objects.get(payment_id=payment_id)
        except Reservation.DoesNotExist:
            return None
        return ReservationModelSerializer(reservation).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['payment_type'] = ItemSerializer(instance.payment_type).data
        data['reservation'] = self.get_reservation_details(instance.id)
        return data


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            'id',
            'commission',
            'subtotal',
            'total',
            'approved_at',
            'payment_type'
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['payment_type'] = ItemSerializer(instance.payment_type).data
        return data


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

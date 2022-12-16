from datetime import datetime

from rest_framework import serializers

from catalogue.serializers import ItemSerializer

from payment.models import Payment

from traveler.models import Traveler
from traveler.serializers import TravelerSerializer

from reservation.models import Reservation, Room, Guest


class GuestModelSerializer(serializers.ModelSerializer):

    traveler = serializers.SerializerMethodField()

    def get_traveler(self, instance):
        return TravelerSerializer(instance.traveler).data

    class Meta:
        model = Guest
        fields = (
            'is_lead',
            'traveler'
        )


class RoomModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'

    def get_guests_details(self, room_id):
        return GuestModelSerializer(
            Guest.objects.filter(room_id=room_id),
            many=True
        ).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['guests'] = self.get_guests_details(instance.id)
        return data


class ReservationModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = '__all__'

    def get_rooms_details(self, reservation_id):
        return RoomModelSerializer(
            Room.objects.filter(reservation_id=reservation_id),
            many=True
        ).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['rooms'] = self.get_rooms_details(instance.id)
        return data


class PaymentDetailSerializer(serializers.ModelSerializer):

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

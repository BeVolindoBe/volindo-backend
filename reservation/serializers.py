from rest_framework import serializers

from payment.serializers import PaymentSerializer


class NewPaymentSerializer(serializers.Serializer):

    commission = serializers.DecimalField(max_digits=10, decimal_places=2)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)


class GuestSerializer(serializers.Serializer):

    traveler_id = serializers.UUIDField()
    is_lead = serializers.BooleanField()


class RoomSerializer(serializers.Serializer):

    guests = GuestSerializer(many=True)
    name = serializers.CharField()


class ReservationSerializer(serializers.Serializer):

    rooms = RoomSerializer(many=True)
    payment = NewPaymentSerializer()
    hotel_id = serializers.UUIDField()
    results_id = serializers.UUIDField()

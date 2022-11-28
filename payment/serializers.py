from rest_framework import serializers

from agent.models import Agent
from agent.serializers import AgentSerializer

from traveler.serializers import TravelerSerializer

from payment.models import ReservationPayment, Reservation


class ReservationSerializer(serializers.ModelSerializer):

    travelers = TravelerSerializer(many=True)

    class Meta:
        model = Reservation
        fields = (
            'hotel_name',
            'check_in',
            'check_out',
            'room_description',
            'travelers'
        )


class ReservationPaymentSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()
    hotels = ReservationSerializer(many=True)

    class Meta:
        model = ReservationPayment
        fields = (
            'agent',
            'amount',
            'commission',
            'total',
            'hotels'
        )

from rest_framework import serializers

from hotel.serializers import HotelSerializer

from traveler.serializers import TravelerSerializer

from reservation.models import Guest, Room, Reservation


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

    hotel = HotelSerializer()

    class Meta:
        model = Reservation
        fields = (
            'id',
            'hotel',
            'policies',
            'policies_acceptance',
            'booking_code',
            'cancelled_at',
            'created_at',
            'updated_at',
            'search_parameters'
        )

    def get_rooms_details(self, reservation_id):
        return RoomModelSerializer(
            Room.objects.filter(reservation_id=reservation_id),
            many=True
        ).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['rooms'] = self.get_rooms_details(instance.id)
        return data


class StringListField(serializers.ListField):
    child = serializers.CharField()


class CancelPoliciesSerializer(serializers.Serializer):
    from_date = serializers.DateField()
    charge = serializers.DecimalField(max_digits=5, decimal_places=2)


class PolicySerializer(serializers.Serializer):
    policy = serializers.CharField()


class PoliciesSerializer(serializers.Serializer):
    cancellation_policies = CancelPoliciesSerializer(many=True)
    policies = StringListField()


class NewPaymentSerializer(serializers.Serializer):

    commission = serializers.DecimalField(max_digits=10, decimal_places=2)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    link = serializers.BooleanField()


class GuestSerializer(serializers.Serializer):

    traveler_id = serializers.UUIDField()
    is_lead = serializers.BooleanField()


class RoomSerializer(serializers.Serializer):

    guests = GuestSerializer(many=True)
    name = serializers.CharField()


class ReservationSerializer(serializers.Serializer):

    rooms = RoomSerializer(many=True)
    payment = NewPaymentSerializer()
    booking_code = serializers.CharField()
    hotel_id = serializers.UUIDField()
    results_id = serializers.UUIDField()
    policies = PoliciesSerializer()
    policies_acceptance = serializers.BooleanField()

    def validate(self, attrs):
        if attrs['policies_acceptance'] is False:
            raise serializers.ValidationError(
                {"policies_acceptance": "User must accept the policies to continue."}
            )
        return attrs

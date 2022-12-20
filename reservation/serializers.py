from rest_framework import serializers


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

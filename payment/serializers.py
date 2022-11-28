from rest_framework import serializers


class TempAgentSerializer(serializers.Serializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()


class TempTravelerSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    birthdate = serializers.DateField()
    phone_number = serializers.CharField()


class ReservationSerializer(serializers.Serializer):
    hotel_name = serializers.CharField()
    room_description = serializers.CharField()
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    guests = TempTravelerSerializer(many=True)


class ReservationPaymentSerializer(serializers.Serializer):

    agent = TempAgentSerializer()
    hotels = ReservationSerializer(many=True)
    amount = serializers.DecimalField(max_digits=10 ,decimal_places=2)
    commission = serializers.DecimalField(max_digits=10 ,decimal_places=2)
    total = serializers.DecimalField(max_digits=10 ,decimal_places=2)

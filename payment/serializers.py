from datetime import datetime

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
    age = serializers.IntegerField()
    phone_number = serializers.CharField()


class ReservationSerializer(serializers.Serializer):
    hotel_name = serializers.CharField()
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    guests = TempTravelerSerializer(many=True)


class ReservationPaymentSerializer(serializers.Serializer):

    agent = TempAgentSerializer()
    hotels = ReservationSerializer(many=True)
    amount = serializers.DecimalField(max_digits=10 ,decimal_places=2)
    commission = serializers.DecimalField(max_digits=10 ,decimal_places=2)
    total = serializers.DecimalField(max_digits=10 ,decimal_places=2)


class CardSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    exp_date = serializers.CharField()
    cvv = serializers.CharField()
    card_name = serializers.CharField()

    def validate(self, attrs):
        if len(attrs['card_number']) != 16:
            raise serializers.ValidationError(
                {"card_number": "Invalid card number."}
            )
        try:
            datetime.strptime('{}-{}-1'.format(
                attrs['exp_date'].split('/')[1], # year yyyy
                attrs['exp_date'].split('/')[0], # month mm
            ), '%Y-%m-%d')
        except ValueError:
            raise serializers.ValidationError(
                {"exp_date": "Invalid expiration date."}
            )
        try:
            int(attrs['cvv'])
        except ValueError:
            raise serializers.ValidationError(
                {"cvv": "Invalid CVV."}
            )
        return attrs

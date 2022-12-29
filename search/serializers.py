from datetime import datetime

from rest_framework import serializers


class SearchRoomSerializer(serializers.Serializer):
    number_of_adults = serializers.IntegerField()
    children_age = serializers.ListField(
        child=serializers.IntegerField()
    )


class SearchHotelSerializer(serializers.Serializer):
    destination = serializers.CharField()
    check_in = serializers.CharField()
    check_out = serializers.CharField()
    rooms = SearchRoomSerializer(many=True)
    currency = serializers.CharField()
    nationality = serializers.CharField()

    def validate(self, attrs):
        now = datetime.now().strftime('%Y-%m-%d')
        if attrs['check_in'] < now or attrs['check_out'] < now or attrs['check_out'] < attrs['check_in']:
            raise serializers.ValidationError(
                {"check_in": "Check in or check out dates are invalid."}
            )
        return attrs


class SearchFlightsSerializer(serializers.Serializer):
    adults = serializers.IntegerField()
    children = serializers.IntegerField()
    infants = serializers.IntegerField()
    flight_type = serializers.CharField()
    flight_class = serializers.CharField()
    origin = serializers.CharField()
    destination = serializers.CharField()
    departure_date = serializers.CharField()
    return_date = serializers.CharField(allow_blank=True)

    def validate(self, attrs):
        now = datetime.now().strftime('%Y-%m-%d')
        if attrs['departure_date'] < now:
            raise serializers.ValidationError(
                {'message': 'Invalid departure_date.'}
            )
        if attrs['return_date'] != '' and attrs['return_date'] < attrs['departure_date']:
            raise serializers.ValidationError(
                {'message': 'return_date must be after departure_date.'}
            )
        return attrs

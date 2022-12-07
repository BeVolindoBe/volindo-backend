from datetime import datetime

from rest_framework import serializers


class SearchRoomSerializer(serializers.Serializer):
    number_of_adults = serializers.IntegerField()
    children_age = serializers.ListField(
        child=serializers.IntegerField()
    )


class SearchSerializer(serializers.Serializer):
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

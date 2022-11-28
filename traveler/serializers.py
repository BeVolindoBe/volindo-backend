from rest_framework import serializers

from catalogue.serializers import ItemSerializer

from traveler.models import Traveler


class TravelerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Traveler
        fields = (
            'first_name',
            'last_name',
            'email',
            'age',
            'phone_number',
            'title'
        )

from rest_framework import serializers

from catalogue.serializers import ItemSerializer

from traveler.models import Traveler


class TravelerSerializer(serializers.ModelSerializer):

    traveler_status = ItemSerializer(read_only=True)
    country = ItemSerializer(read_only=True)
    phone_country_code = ItemSerializer(read_only=True)
    gender = serializers.CharField(
        source='get_gender_display'
    )

    class Meta:
        model = Traveler
        fields = (
            'first_name',
            'last_name',
            'email',
            'birthdate',
            'phone_contry_code',
            'phone_number',
            'gender',
            'traveler_status',
            'in_vacation',
            'is_active',
            'address',
            'country',
            'city',
            'state_province',
            'zip_code'
        )

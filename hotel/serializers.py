from rest_framework import serializers

from hotel.models import Hotel, HotelAmenity, HotelPicture


class HotelPictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelPicture
        fields = (
            'url',
        )


class HotelAmenitySerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelAmenity
        fields = (
            'amenity',
        )


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = (
            'id',
            'address',
            'external_id',
            'destination',
            'hotel_name',
            'stars',
            'latitude',
            'longitude',
            'hotel_amenities',
            'hotel_pictures',
            'description'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['hotel_pictures'] = HotelPictureSerializer(instance.hotel_pictures.all(), many=True).data
        data['hotel_amenities'] = HotelAmenitySerializer(instance.hotel_amenities.all(), many=True).data
        data['destination'] = str(instance.destination)
        return data


class PreBookSerializer(serializers.Serializer):

    booking_code = serializers.CharField()
    results_id = serializers.CharField()

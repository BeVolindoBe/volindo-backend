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

    hotel_amenities = HotelAmenitySerializer(many=True)
    hotel_pictures = HotelPictureSerializer(many=True)

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

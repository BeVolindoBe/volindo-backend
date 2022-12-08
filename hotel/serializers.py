from rest_framework import serializers

from catalogue.serializers import DestinationSerializer

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

    destination = DestinationSerializer()
    hotel_amenities = HotelAmenitySerializer(many=True)
    hotel_pictures = HotelPictureSerializer(many=True)

    class Meta:
        model = Hotel
        fields = (
            'id',
            'address',
            'destination',
            'hotel_name',
            'stars',
            'latitude',
            'longitude',
            'hotel_amenities',
            'hotel_pictures'
        )

from rest_framework import serializers

from catalogue.serializers import ItemSerializer

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

    destination = ItemSerializer()
    hotel_amenities = HotelAmenitySerializer(many=True)
    hotel_pictures = HotelPictureSerializer(many=True)

    class Meta:
        model = Hotel
        fields = (
            'destination',
            'hotel_name',
            'stars',
            'latitude',
            'longitude',
            'hotel_amenities',
            'hotel_pictures'
        )

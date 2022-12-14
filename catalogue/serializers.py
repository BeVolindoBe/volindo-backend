from rest_framework import serializers

from catalogue.models import Catalogue, Item, Destination, Country

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = (
            'id',
            'slug',
            'description'
        )


class CatalogueSerializer(serializers.ModelSerializer):

    items = ItemSerializer(many=True)

    class Meta:
        model = Catalogue
        fields = (
            'slug',
            'description',
            'items',
            'metadata',
        )


class DestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destination
        fields = (
            'id',
            'display_name'
        )


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            'id',
            'iso_code',
            'country_name',
            'metadata',
        )

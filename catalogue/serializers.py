from rest_framework import serializers

from catalogue.models import Catalogue, Item, Destination


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
            'items'
        )


class DestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destination
        fields = (
            'country',
            'display_name'
        )

from rest_framework import serializers

from catalogue.models import Catalogue, Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = (
            'id',
            'slug',
            'description',
            'metadata'
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

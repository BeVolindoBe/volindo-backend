from rest_framework import serializers

from catalog.models import Catalog, Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = [
            'id',
            'catalog',
            'slug',
            'description',
            'metadata'
        ]


class CatalogSerializer(serializers.ModelSerializer):

    items = ItemSerializer(many=True)

    class Meta:
        model = Catalog
        fields = '__all__'

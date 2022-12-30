from rest_framework import serializers

from catalogue.models import Catalogue, Item, Destination, Country


class ItemSerializer(serializers.ModelSerializer):

    id = serializers.CharField()

    class Meta:
        model = Item
        fields = (
            'id',
            'slug',
            'description',
            'metadata'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        return data


class CatalogueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalogue
        fields = (
            'slug',
            'description',
            'items'
        )


class DestinationSerializer(serializers.ModelSerializer):

    id = serializers.CharField()

    class Meta:
        model = Destination
        fields = (
            'id',
            'display_name'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        return data


class CountrySerializer(serializers.ModelSerializer):

    id = serializers.CharField()

    class Meta:
        model = Country
        fields = (
            'id',
            'iso_code',
            'country_name',
            'metadata',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        return data

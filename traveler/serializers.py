from rest_framework import serializers

from catalogue.models import Item
from catalogue.serializers import ItemSerializer, CountrySerializer, Country

from agent.models import Agent

from traveler.models import Traveler


class TravelerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Traveler

        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'phone_country_code',
            'phone_number',
            'title',
            'traveler_status',
            'in_vacation',
            'is_active',
            'address',
            'country',
            'city',
            'state_province',
            'zip_code'
        )
    
    def to_internal_value(self, data):
        try:
            data['country'] = Country.objects.get(id=data['country'])
            data['agent'] = Agent.objects.get(user=self.context['request'].user)
        except KeyError:
            pass
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['country'] = CountrySerializer(instance.country).data
        data['traveler_status'] = ItemSerializer(instance.traveler_status).data
        return data

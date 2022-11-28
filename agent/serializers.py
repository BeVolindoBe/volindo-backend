from rest_framework import serializers

from catalogue.models import Item
from catalogue.serializers import ItemSerializer

from agent.models import Agent


class AgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agent
        fields = (
            'first_name',
            'last_name',
            'email',
            'birthdate',
            'country',
            'phone_country_code',
            'web_site'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['country'] = ItemSerializer(instance.country).data
        data['phone_country_code'] = ItemSerializer(instance.phone_country_code).data
        return data

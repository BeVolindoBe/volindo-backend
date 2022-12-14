from rest_framework import serializers

from catalogue.serializers import CountrySerializer, ItemSerializer

from agent.models import Agent


class AgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agent
        fields = (
            'first_name',
            'last_name',
            'email',
            'photo',
            'phone_country_code',
            'phone_number',
            'birth_date',
            'country',
            'web_site',
            'agent_status',
            'agent_subscription',
        )
        read_only_fields = (
            'agent_status',
            'agent_subscription'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['country'] = CountrySerializer(instance.country).data
        data['phone_country_code'] = ItemSerializer(instance.phone_country_code).data
        data['agent_status'] = ItemSerializer(instance.agent_status).data
        data['agent_subscription'] = ItemSerializer(instance.agent_subscription).data
        return data

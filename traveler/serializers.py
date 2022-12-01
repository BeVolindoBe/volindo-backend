from rest_framework import serializers

from catalogue.serializers import ItemSerializer

from agent.models import Agent

from traveler.models import Traveler


class TravelerSerializer(serializers.ModelSerializer):

    agent_id = serializers.SerializerMethodField()

    class Meta:
        model = Traveler

        fields = (
            'agent_id',
            'first_name',
            'last_name',
            'email',
            'birthdate',
            'age',
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['country'] = ItemSerializer(instance.country).data
        data['phone_country_code'] = ItemSerializer(instance.phone_country_code).data
        data['traveler_status'] = ItemSerializer(instance.agent_status).data
        return data

    def get_agent_id(self, obj):
        return str(Agent.objects.get(user=self.context['request'].user).id)

from rest_framework import serializers

from catalogue.serializers import ItemSerializer

from agent.models import Agent


class AgentSerializer(serializers.ModelSerializer):

    phone_contry_code = ItemSerializer(read_only=True)
    gender = serializers.CharField(
        source='get_gender_display'
    )

    class Meta:
        model = Agent
        fields = (
            'first_name',
            'last_name',
            'email',
            'gender',
            'birthdate',
            'country',
            'phone_contry_code',
            'web_site'
        )

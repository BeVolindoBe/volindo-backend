from rest_framework import serializers

from catalogue.serializers import ItemSerializer

from user.serializers import UserSerializer

from agent.models import Agent


class AgentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    phone_contry_code = ItemSerializer(read_only=True)
    gender = serializers.CharField(
        source='get_gender_display'
    )

    class Meta:
        model = Agent
        fields = (
            'user',
            'first_name',
            'last_name',
            'email',
            'gender',
            'birthday',
            'country',
            'phone_contry_code',
            'web_site'
        )

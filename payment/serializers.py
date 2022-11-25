from rest_framework import serializers

from payment.models import ExternalAgent, Payment, Reservation


class ExternalAgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExternalAgent
        fields = (
            'external_id',
            'agent_name',
            'phone_number',
            'image',
            'agent_email'
        )

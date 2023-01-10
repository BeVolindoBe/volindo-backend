from django.shortcuts import get_object_or_404

from rest_framework.generics import RetrieveUpdateAPIView

from agent.serializers import AgentSerializer
from agent.models import Agent


class AgentDetail(RetrieveUpdateAPIView):

    serializer_class = AgentSerializer
    lookup_field = 'user__external_id'
    queryset = Agent.objects.all()

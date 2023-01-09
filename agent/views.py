from django.shortcuts import get_object_or_404

from rest_framework.generics import RetrieveUpdateAPIView

from agent.serializers import AgentSerializer
from agent.models import Agent


class AgentDetail(RetrieveUpdateAPIView):

    serializer_class = AgentSerializer
    lookup_field = 'user_id'
    queryset = Agent.objects.all()

    # def get_queryset(self):
    #     return Agent.objects.filter(user_id=self.kwargs['user_id'])

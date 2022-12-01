from django.shortcuts import get_object_or_404

from rest_framework.generics import RetrieveUpdateAPIView

from agent.serializers import AgentSerializer
from agent.models import Agent


class AgentDetail(RetrieveUpdateAPIView):

    serializer_class = AgentSerializer

    def get_queryset(self):
        return Agent.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

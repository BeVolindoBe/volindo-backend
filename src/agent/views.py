from rest_framework.generics import RetrieveAPIView

from agent.serializers import AgentSerializer
from agent.models import Agent


class AgentDetail(RetrieveAPIView):

    serializer_class = AgentSerializer
    queryset = Agent.objects.all()

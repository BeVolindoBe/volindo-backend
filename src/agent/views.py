from rest_framework.generics import RetrieveAPIView, CreateAPIView

from agent.serializers import AgentSerializer
from agent.models import Agent


class AgentDetail(RetrieveAPIView):

    serializer_class = AgentSerializer
    queryset = Agent.objects.all()


class NewAgent(CreateAPIView):

    serializer_class = AgentSerializer
    queryset = Agent.objects.all()

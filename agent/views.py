from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from agent.serializers import AgentSerializer
from agent.models import Agent


class AgentDetail(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AgentSerializer
    queryset = Agent.objects.all()

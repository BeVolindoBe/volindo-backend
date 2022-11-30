from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from agent.serializers import AgentSerializer
from agent.models import Agent


class AgentDetail(APIView):

    def get(self, request):
        return Response(
            AgentSerializer(Agent.objects.get(user=request.user)).data,
            status=status.HTTP_200_OK
        )

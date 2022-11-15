from rest_framework.generics import RetrieveAPIView
from rest_framework import status
from rest_framework.response import Response

from traveler.serializers import TravelerSerializer
from traveler.models import Traveler


class TravelerDetail(RetrieveAPIView):

    def get(self, request, agent_id, traveler_id):
        try:
            traveler = Traveler.objects.get(agent_id=agent_id, id=traveler_id)
            return Response(TravelerSerializer(traveler).data, status=status.HTTP_200_OK)
        except Traveler.DoesNotExist:
            return Response(
                {'error': '404', 'message': 'traveler not found'},
                status=status.HTTP_404_NOT_FOUND
            )

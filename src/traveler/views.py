from rest_framework.generics import RetrieveAPIView
from rest_framework import status
from rest_framework.response import Response

from traveler.serializers import TravelerSerializer
from traveler.models import Traveler


class TravelerDetail(RetrieveAPIView):

    serializer_class = TravelerSerializer
    queryset = Traveler.objects.all()

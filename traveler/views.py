from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.response import Response

from traveler.serializers import TravelerSerializer
from traveler.models import Traveler


class TravelerDetail(RetrieveUpdateAPIView):

    serializer_class = TravelerSerializer
    queryset = Traveler.objects.all()

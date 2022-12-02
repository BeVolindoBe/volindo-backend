from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from traveler.serializers import TravelerSerializer
from traveler.models import Traveler


class ListCreateTravelerApiView(ListCreateAPIView):

    serializer_class = TravelerSerializer

    def get_queryset(self):
        return TravelerSerializer.objects.filter(agent__user=self.request.user)


class TravelerDetail(RetrieveUpdateAPIView):

    serializer_class = TravelerSerializer
    queryset = Traveler.objects.all()

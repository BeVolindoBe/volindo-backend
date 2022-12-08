from unidecode import unidecode

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from rest_framework.generics import ListAPIView, RetrieveAPIView

from catalogue.serializers import CatalogueSerializer, DestinationSerializer
from catalogue.models import Catalogue, Destination



class CatalogueList(ListAPIView):

    serializer_class = CatalogueSerializer
    queryset = Catalogue.objects.prefetch_related('items').all()


class CatalogueDetail(RetrieveAPIView):
    serializer_class = CatalogueSerializer
    queryset = Catalogue.objects.prefetch_related('items').all()
    lookup_field = 'slug'


class DestinationAutocomplete(APIView):
    def get(self, request):
        destination = request.query_params.get('destination')
        destinations = Destination.objects.filter(
            search_field__contains=unidecode(destination.lower())
        )
        return Response(DestinationSerializer(destinations, many=True).data, status=status.HTTP_200_OK)

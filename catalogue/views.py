from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from rest_framework.generics import ListAPIView, RetrieveAPIView

from catalogue.serializers import CatalogueSerializer, ItemSerializer
from catalogue.models import Catalogue, Item



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
        destinations = Item.objects.filter(
            description__contains=destination.capitalize(),
            catalogue_id='c807abfe-71ac-11ed-a1eb-0242ac120002'
        )
        return Response(ItemSerializer(destinations, many=True).data, status=status.HTTP_200_OK)

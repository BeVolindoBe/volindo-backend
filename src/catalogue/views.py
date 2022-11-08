from rest_framework.generics import ListAPIView, RetrieveAPIView

from catalogue.serializers import CatalogueSerializer, ItemSerializer
from catalogue.models import Catalogue


class CatalogueListApiView(ListAPIView):

    serializer_class = CatalogueSerializer
    queryset = Catalogue.objects.prefetch_related('items').all()


class CatalogueAPIView(RetrieveAPIView):
    serializer_class = CatalogueSerializer
    queryset = Catalogue.objects.prefetch_related('items').all()
    lookup_field = 'slug'

from rest_framework.generics import ListAPIView, RetrieveAPIView

from catalog.serializers import CatalogSerializer, ItemSerializer
from catalog.models import Catalog


class CatalogListApiView(ListAPIView):

    serializer_class = CatalogSerializer
    queryset = Catalog.objects.prefetch_related('items').all()


class CatalogAPIView(RetrieveAPIView):
    serializer_class = CatalogSerializer
    queryset = Catalog.objects.prefetch_related('items').all()
    lookup_field = 'slug'

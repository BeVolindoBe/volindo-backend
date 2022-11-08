from rest_framework.generics import ListAPIView

from catalog.serializers import CatalogSerializer, ItemSerializer
from catalog.models import Catalog


class CatalogListApiView(ListAPIView):

    serializer_class = CatalogSerializer
    queryset = Catalog.objects.prefetch_related('items').all()

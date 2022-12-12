from rest_framework.generics import RetrieveAPIView

from hotel.models import Hotel
from hotel.serializers import HotelSerializer


class HotelDetail(RetrieveAPIView):
	serializer_class = HotelSerializer
	queryset = Hotel.objects.prefetch_related('hotel_pictures', 'hotel_amenities').all()

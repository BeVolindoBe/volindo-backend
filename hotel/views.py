import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView

from django.core.cache import cache

from hotel.models import Hotel
from hotel.serializers import HotelSerializer


class HotelDetail(RetrieveAPIView):
	serializer_class = HotelSerializer
	queryset = Hotel.objects.prefetch_related('hotel_pictures', 'hotel_amenities').all()
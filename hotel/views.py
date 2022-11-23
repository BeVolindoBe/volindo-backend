import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView

# from django.core.cache import cache

from hotel.models import Hotel
from hotel.serializers import HotelSerializer
# from hotel.tasks.booking import fetch_from_booking
# from hotel.tasks.travelomatix import fetch_from_travelomatix


class HotelDetail(RetrieveAPIView):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.prefetch_related('hotel_pictures', 'hotel_amenities').all()

    # def get(self, request):
    #     data = SearchSerializer(request.data)
    #     print(data)
    #     fetch_from_booking.delay()
    #     fetch_from_travelomatix.delay()
    #     cache.set('test', json.dumps({'hotels': []}), 900)
    #     return Response({'Results': 'test'}, status=status.HTTP_200_OK)

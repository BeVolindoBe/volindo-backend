from uuid import uuid4

import json

from django.core.cache import cache

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from external_api.tasks.tbo.search_hotels import tbo_search_hotels
from external_api.tasks.tmx.search_flights import tmx_search_flights

from search.serializers import SearchHotelSerializer, SearchFlightsSerializer

from hotel.models import Hotel
from hotel.serializers import HotelSerializer


class SearchHotel(APIView):

    def post(self, request):
        filters = SearchHotelSerializer(data=request.data)
        if filters.is_valid(raise_exception=True):
            results_id = str(uuid4())
            results = {
                'results_id': results_id,
                'status': 'pending',
                'filters': filters.data,
                'hotels': []
            }
            cache.set(results_id, json.dumps(results), 900)
            tbo_search_hotels.delay(results_id, filters.data)
            # tbo_search_hotels(results_id, filters.data)
            results['hotels'] = HotelSerializer(
                Hotel.objects.prefetch_related(
                    'hotel_pictures',
                    'hotel_amenities'
                ).filter(destination_id=filters.data['destination']).order_by('?'),
                many=True
            ).data
            return Response(results, status=status.HTTP_200_OK)
        return Response({'message': 'Bad request.'}, status=status.HTTP_400_BAD_REQUEST)


class ResultsHotel(APIView):

    def get(self, request, results_id):
        data = cache.get(results_id)
        if data is None:
            return Response({'message': 'No search results found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(json.loads(data), status=status.HTTP_200_OK)


class SearchFlights(APIView):

    def post(self, request):
        filters = SearchFlightsSerializer(data=request.data)
        if filters.is_valid(raise_exception=True):
            results_id = str(uuid4())
            results = {
                'results_id': results_id,
                'status': 'pending',
                'filters': filters.data,
                'flights': []
            }
            cache.set(results_id, json.dumps(results), 900)
            tmx_search_flights.delay(results_id, filters.data)
            return Response(results, status=status.HTTP_200_OK)
        return Response({'message': 'Bad request.'}, status=status.HTTP_400_BAD_REQUEST)


class ResultsFlights(APIView):

    def get(self, request, results_id):
        data = cache.get(results_id)
        if data is None:
            return Response({'message': 'No search results found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(json.loads(data), status=status.HTTP_200_OK)

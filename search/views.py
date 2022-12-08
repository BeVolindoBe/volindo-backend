from uuid import uuid4

import json

from django.core.cache import cache

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from external_api.tasks.rakuten.search_hotels import search_rakuten
from external_api.tasks.tbo.search_hotels import search_tbo

from search.serializers import SearchSerializer

from hotel.models import Hotel
from hotel.serializers import HotelSerializer


class SearchHotel(APIView):
    @swagger_auto_schema(request_body=SearchSerializer)
    def post(self, request):
        filters = SearchSerializer(data=request.data)
        if filters.is_valid(raise_exception=True):
            results_id = str(uuid4())
            results = {
                'id': results_id,
                'stauts': 'pending',
                'hotels': []
            }
            cache.set(results_id, json.dumps(results), 18000)
            # search_rakuten(results_id, filters.validated_data)
            # search_tbo(results_id, filters.validated_data)
            return Response(results, status=status.HTTP_200_OK)
        error = {
            'message': 'Bad request.'
        }
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


class ResultsHotel(APIView):
    def get(self, request, results_id):
        data = cache.get(results_id)
        if data is None:
            error = {
                'message': 'No search results found.'
            }
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        return Response(json.loads(data), status=status.HTTP_200_OK)

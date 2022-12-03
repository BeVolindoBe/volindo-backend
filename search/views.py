from uuid import uuid4

import json

from django.core.cache import cache

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from external_api.tasks.search_hotels_tbo import search_hotels_tbo


class SearchHotel(APIView):
    def get(self, request):
        results_id = str(uuid4())
        data = {
            'id': results_id,
            'stauts': 'pending',
            'hotels': []
        }
        cache.set(results_id, json.dumps(data), 18000)
        return Response({'results_id': results_id}, status=status.HTTP_200_OK)


class ResultsHotel(APIView):
    def get(self, request, results_id):
        data = cache.get(results_id)
        if data is None:
            error = {
                'message': 'No search results found.'
            }
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        return Response(json.loads(data), status=status.HTTP_200_OK)

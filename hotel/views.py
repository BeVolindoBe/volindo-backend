import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.cache import cache

from hotel.tasks.booking import fetch_from_booking
from hotel.tasks.travelomatix import fetch_from_travelomatix


class Search(APIView):
    def get(self, request):
        fetch_from_booking.delay()
        fetch_from_travelomatix.delay()
        cache.set('test', json.dumps({'hotels': []}), 900)
        return Response({'Results': 'test'}, status=status.HTTP_200_OK)


class Result(APIView):
    def get(self, request):
        data = json.loads(cache.get('test'))
        return Response(data, status=status.HTTP_200_OK)

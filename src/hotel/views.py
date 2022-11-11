from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from hotel.tasks.booking import fetch_from_booking
from hotel.tasks.travelomatix import fetch_from_travelomatix


class Search(APIView):
    def get(self, request):
        fetch_from_booking.delay()
        fetch_from_travelomatix.delay()
        return Response({'hola': 'mundo'}, status=status.HTTP_200_OK)

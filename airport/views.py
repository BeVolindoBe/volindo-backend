from unidecode import unidecode

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from airport.models import Airport
from airport.serializers import AirportSerializer


class AirportAutocomplete(APIView):
    def get(self, request):
        airport = request.query_params.get('airport')
        if airport is not None:
            airports = Airport.objects.filter(
                search_field__contains=unidecode(airport.lower())
            )
            return Response(AirportSerializer(airports, many=True).data, status=status.HTTP_200_OK)
        return Response({'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

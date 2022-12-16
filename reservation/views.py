from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from reservation.serializers import ReservationSerializer

from external_api.tasks.tbo.book import tbo_book


class Reservation(APIView):

    @swagger_auto_schema(request_body=ReservationSerializer)
    def post(self, request):
        data = ReservationSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            response = tbo_book(data)
            return Response(response.data, status=response.status_code)

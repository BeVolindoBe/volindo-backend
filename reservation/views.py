from datetime import datetime

import json

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from reservation.models import Reservation
from reservation.serializers import ReservationSerializer, ReservationModelSerializer

from payment.serializers import PaymentDetailSerializer
from payment.models import Payment

from external_api.tasks.tbo.book import tbo_book


class ReservationApiView(APIView):

    @swagger_auto_schema(request_body=ReservationSerializer)
    def post(self, request):
        data = ReservationSerializer(data=request.data)
        if data.is_valid(raise_exception=True):
            cleaned_data = data.data
            results = cache.get(cleaned_data['results_id'])
            if results is None:
                return Response({'message': 'Data is no longer available.'}, status=status.HTTP_404_NOT_FOUND)
            cleaned_data['filters'] = json.loads(results)['filters']
            response = tbo_book(cleaned_data, request.user)
            return Response(response.data, status=response.status_code)
    
    def get(self, request):
        response_data = PaymentDetailSerializer(
            Payment.objects.filter(agent__user=request.user),
            many=True
        ).data
        return Response(response_data, status=status.HTTP_200_OK)


class CancelReservationApiView(APIView):
    def post(self, request, reservation_id):
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.cancelled_at = datetime.now()
        reservation.save()
        data = ReservationModelSerializer(reservation).data
        return Response(data, status=status.HTTP_200_OK)

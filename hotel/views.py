from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from external_api.tasks.tbo.hotel_details import tbo_hotel_details


class HotelDetail(APIView):
	def get(self, request, pk):
		if request.query_params.get('results_id') is None:
			return Response(
				{
					'status_code': 400,
					'message': 'Bad request. Invalid results_id parameter.'
				},
				status=status.HTTP_400_BAD_REQUEST
			)
		data = tbo_hotel_details(pk, request.query_params.get('results_id'))
		return Response(data.data, status=data.status_code)

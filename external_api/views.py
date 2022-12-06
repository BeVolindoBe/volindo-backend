from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from external_api.tasks.rakuten.static_data import rakuten_data


class ExternalDataView(APIView):
    def get(self, request):
        rakuten_data()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

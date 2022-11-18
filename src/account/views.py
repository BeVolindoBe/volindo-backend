from django.contrib.auth.models import User

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer


class HealthCheck(APIView):
    def get(self, request):
        return Response({'Message': 'OK'}, status=status.HTTP_200_OK)

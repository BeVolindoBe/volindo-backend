from django.contrib.auth.models import User

from rest_framework.generics import CreateAPIView

from user.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer

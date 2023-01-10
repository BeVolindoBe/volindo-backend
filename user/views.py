from rest_framework.generics import CreateAPIView, RetrieveAPIView

from user.models import User
from user.serializers import UserSerializer


class NewAccount(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountDetail(RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.get_queryset().get(id=self.kwargs['external_id'])

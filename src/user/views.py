from rest_framework.generics import RetrieveAPIView

from user.serializers import UserSerializer
from user.models import User


class UserDetail(RetrieveAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related('user_status').all()

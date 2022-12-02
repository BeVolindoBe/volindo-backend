from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from notification.models import Notification
from notification.serializers import NotificationSerializer


class NotificationDetail(RetrieveUpdateAPIView):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationList(ListAPIView):

    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(agent__user=self.request.user, read=False)

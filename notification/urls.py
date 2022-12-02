from django.urls import path

from notification.views import NotificationDetail, NotificationList


urlpatterns = [
    path('', NotificationList.as_view()),
    path('<str:pk>/', NotificationDetail.as_view()),
]

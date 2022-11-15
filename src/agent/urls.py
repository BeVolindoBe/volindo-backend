from django.urls import path

from user.views import UserDetail


urlpatterns = [
    path('<str:pk>', UserDetail.as_view())
]

from django.urls import path

from traveler.views import TravelerDetail


urlpatterns = [
    path('<str:pk>', TravelerDetail.as_view())
]

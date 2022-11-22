from django.urls import path

from hotel.views import HotelsList


urlpatterns = [
    path('<str:destination__slug>/', HotelsList.as_view()),
]

from django.urls import path

from hotel.views import HotelDetail


urlpatterns = [
    path('<str:pk>/', HotelDetail.as_view()),
]

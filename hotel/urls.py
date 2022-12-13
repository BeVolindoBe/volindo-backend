from django.urls import path

from hotel.views import HotelDetail, PreBook


urlpatterns = [
    path('rooms/prebook/', PreBook.as_view()),
    path('<str:pk>/', HotelDetail.as_view()),
]

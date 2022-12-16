from django.urls import path

from reservation.views import Reservation


urlpatterns = [
    path('', Reservation.as_view())
]

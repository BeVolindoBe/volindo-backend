from django.urls import path

from reservation.views import ReservationApiView


urlpatterns = [
    path('', ReservationApiView.as_view())
]

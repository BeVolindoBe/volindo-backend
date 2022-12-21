from django.urls import path

from reservation.views import ReservationApiView, CancelReservationApiView


urlpatterns = [
    path('', ReservationApiView.as_view()),
    path('<str:reservation_id>/cancel/', CancelReservationApiView.as_view()),
]

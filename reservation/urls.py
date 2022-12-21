from django.urls import path

from reservation.views import ReservationApiView, CancelReservationApiView


urlpatterns = [
    path('', ReservationApiView.as_view()),
    path('<str:pk>/cancel/', CancelReservationApiView.as_view()),
]

from django.urls import path

from payment.views import NewReservationPayment


urlpatterns = [
    path('reservations/', NewReservationPayment.as_view()),
]

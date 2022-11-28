from django.urls import path

from payment.views import ReservationPayment


urlpatterns = [
    path('reservation-payment/', ReservationPayment.as_view()),
]

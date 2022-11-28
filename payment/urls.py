from django.urls import path

from payment.views import NewReservationPayment, PaymentView


urlpatterns = [
    path('reservations/', NewReservationPayment.as_view()),
    path('<str:payment_id>/', PaymentView.as_view()),
]

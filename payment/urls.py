from django.urls import path

from payment.views import PaymentList, PaymentDetail, ReservationPayment


urlpatterns = [
   path('', PaymentList.as_view()),
   path('<str:pk>/', PaymentDetail.as_view()),
   path('<str:pk>/reservation/', ReservationPayment.as_view()),
]

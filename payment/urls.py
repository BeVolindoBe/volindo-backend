from django.urls import path

from payment.views import PaymentList, PaymentDetail


urlpatterns = [
   path('', PaymentList.as_view()),
   path('<str:pk>/', PaymentDetail.as_view()),
]

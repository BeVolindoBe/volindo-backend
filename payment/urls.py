from django.urls import path

from payment.views import PaymentList


urlpatterns = [
   path('', PaymentList.as_view())
]

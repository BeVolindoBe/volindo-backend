from django.urls import path

from payment.views import NewExternalAgent, payment_link


urlpatterns = [
    path('<str:payment_id/', payment_link),
    path('external_agents/', NewExternalAgent.as_view()),
]

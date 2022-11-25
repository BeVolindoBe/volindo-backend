from django.urls import path

from payment.views import NewExternalAgent, payment_link


urlpatterns = [
    path('external_agents/', NewExternalAgent.as_view()),
    path('<str:payment_id>/', payment_link),
]

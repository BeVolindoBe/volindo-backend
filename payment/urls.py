from django.urls import path

from payment.views import NewExternalAgent, payment_link, payment_edit


urlpatterns = [
    path('external_agents/', NewExternalAgent.as_view()),
    path('<str:payment_id>/', payment_link),
    path('<str:payment_id>/edit/', payment_edit),
]

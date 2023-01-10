from django.urls import path, include

from agent.views import AgentDetail


urlpatterns = [
    path('<str:user__external_id>/travelers/', include('traveler.urls')),
    path('<str:user__external_id>/notifications/', include('notification.urls')),
    path('<str:user__external_id>/reservations/', include('reservation.urls')),
    path('<str:user__external_id>/payments/', include('payment.urls')),
    path('<str:user__external_id>/', AgentDetail.as_view()),
]

from django.urls import path, include

from agent.views import AgentDetail


urlpatterns = [
    path('<str:user_id>/travelers/', include('traveler.urls')),
    path('<str:user_id>/notifications/', include('notification.urls')),
    path('<str:user_id>/reservations/', include('reservation.urls')),
    path('<str:user_id>/payments/', include('payment.urls')),
    path('<str:user_id>/', AgentDetail.as_view()),
]

from django.urls import path, include

from agent.views import AgentDetail


urlpatterns = [
    path('', AgentDetail.as_view()),
    path('travelers/', include('traveler.urls')),
    path('notifications/', include('notification.urls')),
    path('reservations/', include('reservation.urls')),
    path('payments/', include('payment.urls')),
]

from django.urls import path

from agent.views import AgentDetail


urlpatterns = [
    path('<str:pk>', AgentDetail.as_view())
]

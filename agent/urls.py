from django.urls import path

from agent.views import AgentDetail


urlpatterns = [
    path('', AgentDetail.as_view())
]

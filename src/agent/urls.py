from django.urls import path

from agent.views import AgentDetail, NewAgent


urlpatterns = [
    path('', NewAgent.as_view()),
    path('<str:pk>/', AgentDetail.as_view())
]

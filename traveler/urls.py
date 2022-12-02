from django.urls import path

from traveler.views import ListCreateTravelerApiView, TravelerDetail


urlpatterns = [
    path('', ListCreateTravelerApiView.as_view()),
    path('<str:pk>/', TravelerDetail.as_view()),
]

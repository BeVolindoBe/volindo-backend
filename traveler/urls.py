from django.urls import path

from traveler.views import ListCreateTravelerApiView


urlpatterns = [
    path('', ListCreateTravelerApiView.as_view()),
]

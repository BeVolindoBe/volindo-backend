from django.urls import path

from traveler.views import TravelerDetail


urlpatterns = [
    path('<str:traveler_id>', TravelerDetail.as_view())
]

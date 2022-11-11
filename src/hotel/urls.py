from django.urls import path

from hotel.views import Search


urlpatterns = [
    path('search', Search.as_view()),
]

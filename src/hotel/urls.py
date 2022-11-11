from django.urls import path

from hotel.views import Search, Result


urlpatterns = [
    path('search', Search.as_view()),
    path('results', Result.as_view()),
]

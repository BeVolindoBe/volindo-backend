from django.contrib import admin
from django.urls import path, include

from account.views import HealthCheck


urlpatterns = [
    path('', HealthCheck.as_view()),
    path('users/', include('agent.urls')),
    path('accounts/', include('user.urls')),
    path('catalogues/', include('catalogue.urls')),
    path('search/', include('search.urls')),
    path('bank-accounts/', include('bank.urls')),
    path('hotels/', include('hotel.urls')),
]

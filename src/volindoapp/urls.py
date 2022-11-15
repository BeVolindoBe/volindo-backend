from django.urls import path, include


urlpatterns = [
    path('catalogues/', include('catalogue.urls')),
    path('agents/<str:agent_id>/travelers/', include('traveler.urls')),
    path('agents/', include('agent.urls')),
    path('hotels/', include('hotel.urls')),
]

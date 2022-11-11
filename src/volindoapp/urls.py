from django.urls import path, include


urlpatterns = [
    path('catalogues/', include('catalogue.urls')),
    path('hotels/', include('hotel.urls'))
]

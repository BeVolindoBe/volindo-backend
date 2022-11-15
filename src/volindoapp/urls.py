from django.urls import path, include


urlpatterns = [
    path('catalogues/', include('catalogue.urls')),
    path('users/', include('user.urls')),
    path('hotels/', include('hotel.urls'))
]

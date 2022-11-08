from django.urls import path, include


urlpatterns = [
    path('catalogs/', include('catalog.urls')),
]

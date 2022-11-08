from django.urls import path

from catalog.views import CatalogListApiView


urlpatterns = [
    path('all/', CatalogListApiView.as_view()),
]

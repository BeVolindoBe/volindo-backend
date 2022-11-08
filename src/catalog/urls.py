from django.urls import path

from catalog.views import CatalogListApiView, CatalogAPIView


urlpatterns = [
    path('all', CatalogListApiView.as_view()),
    path('<str:slug>', CatalogAPIView.as_view()),
]

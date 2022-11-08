from django.urls import path

from catalogue.views import CatalogueListApiView, CatalogueAPIView


urlpatterns = [
    path('all', CatalogueListApiView.as_view()),
    path('<str:slug>', CatalogueAPIView.as_view()),
]

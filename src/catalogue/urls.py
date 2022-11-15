from django.urls import path

from catalogue.views import CatalogueDetail, CatalogueList


urlpatterns = [
    path('all/', CatalogueList.as_view()),
    path('<str:slug>/', CatalogueDetail.as_view()),
]

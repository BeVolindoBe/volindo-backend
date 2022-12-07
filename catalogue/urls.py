from django.urls import path

from catalogue.views import CatalogueDetail, CatalogueList, DestinationAutocomplete


urlpatterns = [
    path('all/', CatalogueList.as_view()),
    path('destinations/', DestinationAutocomplete.as_view()),
    path('<str:slug>/', CatalogueDetail.as_view()),
]

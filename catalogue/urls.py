from django.urls import path

from catalogue.views import CatalogueDetail, CatalogueList, DestinationAutocomplete, CountryList


urlpatterns = [
    path('all/', CatalogueList.as_view()),
    path('countries/', CountryList.as_view()),
    path('destinations/', DestinationAutocomplete.as_view()),
    path('<str:slug>/', CatalogueDetail.as_view()),
]

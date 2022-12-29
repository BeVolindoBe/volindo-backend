from django.urls import path

from catalogue.views import CatalogueDetail, CatalogueList, DestinationAutocomplete, CountryList

from airport.views import AirportAutocomplete


urlpatterns = [
    path('all/', CatalogueList.as_view()),
    path('countries/', CountryList.as_view()),
    path('destinations/', DestinationAutocomplete.as_view()),
    path('airports/', AirportAutocomplete.as_view()),
    path('<str:slug>/', CatalogueDetail.as_view()),
]

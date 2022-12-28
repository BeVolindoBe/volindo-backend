from django.urls import path

from search.views import SearchHotel, ResultsHotel, SearchFlights, ResultsFlights


urlpatterns = [
    path('hotels/', SearchHotel.as_view()),
    path('hotels/results/<str:results_id>/', ResultsHotel.as_view()),
    path('flights/', SearchFlights.as_view()),
    path('flights/results/<str:results_id>/', ResultsFlights.as_view())
]

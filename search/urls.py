from django.urls import path

from search.views import SearchHotel, ResultsHotel


urlpatterns = [
    path('hotels/', SearchHotel.as_view()),
    path('hotels/results/<str:results_id>/', ResultsHotel.as_view())
]

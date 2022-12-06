from django.urls import path

from external_api.views import ExternalDataView


urlpatterns = [
    path('static/', ExternalDataView.as_view())
]

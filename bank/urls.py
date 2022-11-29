from django.urls import path

from bank.views import BankList


urlpatterns = [
    path('', BankList.as_view())
]

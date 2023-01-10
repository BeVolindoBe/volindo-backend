from django.urls import path

from user.views import NewAccount, AccountDetail


urlpatterns = [
    path('', NewAccount.as_view()),
    path('<str:external_id>/', AccountDetail.as_view())
]

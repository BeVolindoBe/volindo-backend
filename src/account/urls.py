from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account.views import RegisterView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('register/', RegisterView.as_view())
]

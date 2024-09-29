# your_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    TransactionViewSet,
    AccountViewSet,
    CustomObtainAuthToken,
    TokenDetailView,
    UserRegistrationView,  # Import the registration view
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"accounts", AccountViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "api-token-auth/", CustomObtainAuthToken.as_view(), name="api-token-auth"
    ),  # Endpoint to obtain a token
    path(
        "token/", TokenDetailView.as_view(), name="token-detail"
    ),  # Endpoint to retrieve token for authenticated user
    path(
        "register/", UserRegistrationView.as_view(), name="register"
    ),  # Registration endpoint
]

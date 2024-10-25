# your_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    TransactionViewSet,
    AccountViewSet,
    CustomObtainAuthToken,
    TokenDetailView,
    UserRegistrationView,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"accounts", AccountViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

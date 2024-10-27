from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookEntryViewSet,
    TransactionViewSet,
    AccountViewSet,
    UserAccountBalanceViewSet,
)

router = DefaultRouter()

router.register(r"transactions", TransactionViewSet)
router.register(r"accounts", AccountViewSet)
router.register(r"user-accounts-balances", UserAccountBalanceViewSet)
router.register(r"book-entries", BookEntryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

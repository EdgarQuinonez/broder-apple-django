from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"users", views.UserViewSet, basename="user")
router.register(r"transactions", views.TransactionViewSet, basename="transaction")
router.register(r"accounts", views.AccountViewSet, basename="account")


urlpatterns = [
    path("", include(router.urls)),
]

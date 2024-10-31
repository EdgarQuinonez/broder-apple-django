from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    LogViewSet,
    InventoryViewSet,
    SaleViewSet,
)

router = DefaultRouter()

router.register(r"products", ProductViewSet)
router.register(r"logs", LogViewSet)
router.register(r"inventory", InventoryViewSet)
router.register(r"sales", SaleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

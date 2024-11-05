from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BrandViewSet,
    CarrierViewSet,
    ConditionViewSet,
    ProductModelViewSet,
    ProductViewSet,
    LogViewSet,
    InventoryViewSet,
    SaleViewSet,
    StorageViewSet,
)

router = DefaultRouter()

router.register(r"products", ProductViewSet)
router.register(r"logs", LogViewSet)
router.register(r"inventory", InventoryViewSet)
router.register(r"sales", SaleViewSet)
router.register(r"brands", BrandViewSet)
router.register(r"storage", StorageViewSet)
router.register(r"product_models", ProductModelViewSet)
router.register(r"conditions", ConditionViewSet)
router.register(r"carriers", CarrierViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

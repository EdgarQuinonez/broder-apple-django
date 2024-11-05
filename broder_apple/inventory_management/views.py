from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Product, Log, Inventory, Sale
from .serializers import (
    ProductSerializer,
    LogSerializer,
    InventorySerializer,
    SaleSerializer,
)
from rest_framework.permissions import IsAuthenticated


from rest_framework import viewsets
from .models import Brand, Storage, ProductModel, Condition, Carrier
from .serializers import (
    BrandSerializer,
    StorageSerializer,
    ProductModelSerializer,
    ConditionSerializer,
    CarrierSerializer,
)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "id"


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    lookup_field = "id"


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer
    lookup_field = "id"

    # Optional filtering based on brand
    def get_queryset(self):
        brand_id = self.request.query_params.get("brand_id")
        if brand_id:
            return self.queryset.filter(brand_id=brand_id)
        return self.queryset


class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    lookup_field = "id"

    # Optional filtering based on category
    def get_queryset(self):
        category = self.request.query_params.get("category")
        if category:
            return self.queryset.filter(category=category)
        return self.queryset


class CarrierViewSet(viewsets.ModelViewSet):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    lookup_field = "id"


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Product instances.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class LogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Log entries related to products.
    """

    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "product"

    def perform_create(self, serializer):
        # Customize save behavior if needed
        serializer.save()


class InventoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Inventory instances.
    """

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "product"

    def perform_create(self, serializer):
        # Customize save behavior if needed
        serializer.save()


class SaleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Sale instances.
    """

    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "product"

    def perform_create(self, serializer):
        # Customize save behavior if needed
        serializer.save()

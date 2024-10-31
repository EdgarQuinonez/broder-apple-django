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

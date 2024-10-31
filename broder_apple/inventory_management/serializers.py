from rest_framework import serializers
from .models import Product, Log, Inventory, Sale


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "brand",
            "model",
            "storage_capacity",
            "carrier",
            "battery_health",
            "screen",
            "sidesAndBack",
            "fullyFunctional",
            "repaired",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class LogSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Log
        fields = [
            "product",
            "listed_price",
            "shipping_cost",
            "platform",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class InventorySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Inventory
        fields = [
            "product",
            "listed_price",
            "shipping_cost",
            "platform",
            "buyout_price",
            "estimated_sale_price",
            "seller",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class SaleSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Sale
        fields = [
            "product",
            "listed_price",
            "shipping_cost",
            "platform",
            "buyout_price",
            "estimated_sale_price",
            "seller",
            "sale_price",
            "buyer",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

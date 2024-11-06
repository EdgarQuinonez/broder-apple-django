from rest_framework import serializers
from .models import Product, Log, Inventory, Sale


from rest_framework import serializers
from .models import Brand, Storage, ProductModel, Condition, Carrier


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ["id", "capacity"]


class ProductModelSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), source="brand", write_only=True
    )
    storage_options = StorageSerializer(many=True, read_only=True)
    storage_options_ids = serializers.PrimaryKeyRelatedField(
        queryset=Storage.objects.all(),
        source="storage_options",
        many=True,
        write_only=True,
    )

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "name",
            "brand",
            "brand_id",
            "storage_options",
            "storage_options_ids",
        ]


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ["id", "category", "condition", "description"]


class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "model",
            "storage_capacity",
            "carrier",
            "battery_health",
            "screen_condition",
            "sides_and_back_condition",
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
            "is_listed",
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

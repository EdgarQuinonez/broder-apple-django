from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Brand(models.Model):
    """
    Model representing the brand of the product.
    """

    name = models.CharField(max_length=180, unique=True)

    def __str__(self):
        return self.name


class Storage(models.Model):
    """
    Model representing storage options for products.
    """

    capacity = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.capacity


class ProductModel(models.Model):
    """
    Model representing specific models of a product, linked to a brand.
    """

    name = models.CharField(max_length=180)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")
    storage_options = models.ManyToManyField(Storage, related_name="product_models")

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class Condition(models.Model):
    """
    Generalized model for conditions of different parts of a product.
    """

    category = models.CharField(max_length=50)  # e.g., "Screen", "SidesAndBack"
    condition = models.CharField(max_length=50)  # e.g., "Cracked", "Good"
    description = models.TextField()

    def __str__(self):
        return f"{self.category} - {self.condition}"


class Carrier(models.Model):
    """
    Model representing carrier options for products.
    """

    name = models.CharField(max_length=180, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Main product model with dynamic fields for brand, model, storage, and condition.
    """

    title = models.CharField(max_length=180)
    description = models.TextField()
    model = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    storage_capacity = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    carrier = models.ForeignKey(
        "Carrier",
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    battery_health = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        default=100,
    )
    screen_condition = models.ForeignKey(
        Condition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category": "Pantalla"},
        related_name="screen_products",
    )
    sides_and_back_condition = models.ForeignKey(
        Condition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"category": "Lados y tapa"},
        related_name="sides_back_products",
    )
    fullyFunctional = models.BooleanField(null=True, blank=True, default=True)
    repaired = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated_at"]

    def __str__(self):
        return self.title


class Log(models.Model):
    MERCADO_LIBRE = "ml"
    FACEBOOK_MARKETPLACE = "fb"
    PLATFORM_CHOICES = [
        (MERCADO_LIBRE, "Mercado Libre"),
        (FACEBOOK_MARKETPLACE, "Facebook Marketplace"),
    ]

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="log"
    )
    listed_price = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2)
    platform = models.CharField(max_length=32, choices=PLATFORM_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated_at"]


class Inventory(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="inventory"
    )
    listed_price = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2)
    platform = models.CharField(max_length=32, choices=Log.PLATFORM_CHOICES)
    buyout_price = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    is_listed = models.BooleanField(default=False)
    seller = models.CharField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated_at"]


class Sale(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="sales"
    )
    listed_price = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2)
    platform = models.CharField(max_length=32, choices=Log.PLATFORM_CHOICES)
    buyout_price = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    seller = models.CharField(max_length=180)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    buyer = models.CharField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated_at"]

from django.db import models


# Create your models here.
class Product(models.Model):

    UNLOCKED = "unlocked"

    CARRIER_CHOICES = [
        (UNLOCKED, "Unlocked"),
    ]

    """
    Pantalla
    Dañada:
    Crack en la pantalla o defectuosa (ej. ghost touch, screen burn-in, dead pixels). Puede tener rayones visibles a simple vista. Puede tener problemas de funcionamiento.
    Aceptable:
    Ningún Crack. Puede tener rayones visibles a simple vista con la pantalla apagada. La pantalla no tiene pixeles defectuosos (ej. ghost touch, screen burn-in, dead pixels), y funciona perfectamente.
    Buena:
    Ningún Crack. Tiene rayones muy leves que no se ven a simple vista. La pantalla no tiene pixeles defectuosos (ej. ghost touch, screen burn-in, dead pixels), y funciona perfectamente.
    Impecable:
    No hay ningún rayón visible. La pantalla no tiene pixeles defectuosos (ej. ghost touch, screen burn-in, dead pixels), y funciona perfectamente.
    """

    CRACKED = "cracked"
    USED = "used"
    GOOD = "good"
    FLAWLESS = "flawless"

    SCREEN_CHOICES = [
        (CRACKED, "Dañada"),
        (USED, "Aceptable"),
        (GOOD, "Buena"),
        (FLAWLESS, "Impecable"),
    ]

    """
    Lados y atrás
    Dañada:
    Crack en la parte de atrás.
    Aceptable:
    Desgaste visible, golpes y abolladuras.
    Buena:
    Descarapelado sin golpes ni abolladuras.
    Impecable:
    Como nuevo.
    """

    # TODO: Due to the different descriptions, do I need to create Models for Screen and SidesAndBack options?

    SIDES_AND_BACK_CHOICES = [
        (CRACKED, "Dañada"),
        (USED, "Aceptable"),
        (GOOD, "Buena"),
        (FLAWLESS, "Impecable"),
    ]

    # TODO: Change the mock up options to the actual dataset of smartphones
    APPLE = "apple"
    SAMSUNG = "samsung"

    BRAND_CHOICES = [
        (APPLE, "Apple"),
        (SAMSUNG, "Samsung"),
    ]

    IPHONE_11 = "ip11"
    IPHONE_12 = "ip12"
    IPHONE_12_PRO = "ip12p"
    IPHONE_12_PRO_MAX = "ip12pm"
    IPHONE_13 = "ip13"
    IPHONE_13_PRO = "ip13p"
    IPHONE_13_PRO_MAX = "ip13pm"
    IPHONE_14 = "ip14"
    IPHONE_14_PRO = "ip14p"
    IPHONE_14_PRO_MAX = "ip14pm"
    GALAXY_S20 = "gs20"

    MODEL_CHOICES = [
        (IPHONE_11, "iPhone 11"),
        (IPHONE_12, "iPhone 12"),
        (IPHONE_12_PRO, "iPhone 12 Pro"),
        (IPHONE_12_PRO_MAX, "iPhone 12 Pro Max"),
        (IPHONE_13, "iPhone 13"),
        (IPHONE_13_PRO, "iPhone 13 Pro"),
        (IPHONE_13_PRO_MAX, "iPhone 13 Pro Max"),
        (IPHONE_14, "iPhone 14"),
        (IPHONE_14_PRO, "iPhone 14 Pro"),
        (IPHONE_14_PRO_MAX, "iPhone 14 Pro Max"),
        (GALAXY_S20, "Galaxy S20"),
    ]

    STORAGE_128GB = "128"
    STORAGE_64GB = "64"
    STORAGE_256GB = "256"
    STORAGE_512GB = "512"
    STORAGE_1TB = "1024"

    STORAGE_CHOICES = [
        (STORAGE_64GB, "64GB"),
        (STORAGE_128GB, "128GB"),
        (STORAGE_256GB, "256GB"),
        (STORAGE_512GB, "512GB"),
        (STORAGE_1TB, "1TB"),
    ]

    title = models.CharField(max_length=180)
    description = models.TextField()
    brand = models.CharField(max_length=32, choices=BRAND_CHOICES)
    model = models.CharField(max_length=32, choices=MODEL_CHOICES)
    storage_capacity = models.CharField(max_length=32, choices=STORAGE_CHOICES)
    carrier = models.CharField(max_length=32, choices=CARRIER_CHOICES)
    battery_health = models.IntegerField(max=100)
    screen = models.CharField(max_length=32, choices=SCREEN_CHOICES)
    sidesAndBack = models.CharField(max_length=32, choices=SIDES_AND_BACK_CHOICES)
    fullyFunctional = models.BooleanField()
    repaired = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated_at"]


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
    platform = models.CharField(max_length=32, choices=Product.PLATFORM_CHOICES)
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
    platform = models.CharField(max_length=32, choices=Product.PLATFORM_CHOICES)
    buyout_price = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_sale_price = models.DecimalField(max_digits=12, decimal_places=2)
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
    platform = models.CharField(max_length=32, choices=Product.PLATFORM_CHOICES)
    buyout_price = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    seller = models.CharField(max_length=180)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    buyer = models.CharField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated_at"]

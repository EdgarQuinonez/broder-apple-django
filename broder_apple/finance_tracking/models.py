from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"

    # Predefined Accounts Mapping
    CASH = 1
    BANK = 2
    OTHER_INCOME = 3
    PERSONAL_EXPENSES = 4
    PURCHASES = 5
    SALES_REVENUE = 6
    SALES_COST = 7

    NATURE_CHOICES = [
        (ASSET, "Asset"),
        (LIABILITY, "Liability"),
        (EQUITY, "Equity"),
        (REVENUE, "Revenue"),
        (EXPENSE, "Expense"),
    ]

    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    nature = models.CharField(max_length=9, choices=NATURE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class UserAccountBalance(models.Model):
    """Intermediate model to manage user-specific balances for each Account."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_account_balances"
    )
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="user_balances"
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ("user", "account")


class Transaction(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    PURCHASE = "purchase"
    SALE = "sale"

    TYPE_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
        (PURCHASE, "Purchase"),
        (SALE, "Sale"),
    ]

    CASH = "cash"
    BANK = "bank"

    PAYMENT_METHOD_CHOICES = [
        (CASH, "Cash"),
        (BANK, "Bank"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]


class BookEntry(models.Model):
    DEBIT = "debit"
    CREDIT = "credit"

    BALANCE_CHOICES = [
        (DEBIT, "Debit"),
        (CREDIT, "Credit"),
    ]

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user_account_balance = models.ForeignKey(
        UserAccountBalance, on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_type = models.CharField(max_length=6, choices=BALANCE_CHOICES)

class Product(models.Model):
    MERCADO_LIBRE = "ml"
    FACEBOOK_MARKETPLACE = "fb"
    
    PLATFORM_CHOICES = [
        (MERCADO_LIBRE, "Mercado Libre"),
        (FACEBOOK_MARKETPLACE, "Facebook Marketplace"),
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
    platform = models.CharField(max_length=32, choices=PLATFORM_CHOICES)
    brand = models.CharField(max_length=32, choices=BRAND_CHOICES)
    model = models.CharField(max_length=32, choices=MODEL_CHOICES)
    storage_capacity = models.CharField(max_length=32, choices=STORAGE_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
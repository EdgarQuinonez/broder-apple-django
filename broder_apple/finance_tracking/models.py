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
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

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

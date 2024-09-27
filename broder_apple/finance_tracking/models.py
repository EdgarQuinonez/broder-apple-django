from django.db import models


class Transaction(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    CASH = "cash"
    BANK = "bank"

    TYPE_CHOICES = [(INCOME, "Income"), (EXPENSE, "Expense")]
    PAYMENT_METHOD_CHOICES = [(CASH, "Cash"), (BANK, "Bank")]

    owner = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="transactions"
    )
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=7, choices=PAYMENT_METHOD_CHOICES)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.description}"

    class Meta:
        ordering = ["-updated_at"]


class BookEntry(models.Model):
    DEBIT = "debit"
    CREDIT = "credit"
    BALANCE_CHOICES = [(DEBIT, "Debit"), (CREDIT, "Credit")]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_type = models.CharField(max_length=6, choices=BALANCE_CHOICES)
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    transaction = models.ForeignKey("Transaction", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.account.name} - {self.balance_type} - {self.amount}"


class Account(models.Model):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"

    NATURE_CHOICES = [
        (ASSET, "Asset"),
        (LIABILITY, "Liability"),
        (EQUITY, "Equity"),
        (REVENUE, "Revenue"),
        (EXPENSE, "Expense"),
    ]

    owner = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="accounts"
    )
    name = models.CharField(max_length=100)
    nature = models.CharField(max_length=9, choices=NATURE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

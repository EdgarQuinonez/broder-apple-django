from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from finance_tracking.models import Account, BookEntry, Transaction, UserAccountBalance


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Transaction
        fields = [
            "id",
            "user",
            "transaction_type",
            "description",
            "amount",
            "payment_method",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            transaction_instance = Transaction.objects.create(**validated_data)

            payment_method = validated_data.get("payment_method")
            amount = validated_data.get("amount")
            user = transaction_instance.user

            try:
                # Determine payment method account (cash or bank)
                if payment_method == "cash":
                    payment_method_account = Account.objects.get(id=Account.CASH)
                elif payment_method == "bank":
                    payment_method_account = Account.objects.get(id=Account.BANK)
                else:
                    raise serializers.ValidationError("Invalid payment method provided.")

                # Handle different transaction types
                if transaction_instance.transaction_type == Transaction.INCOME:
                    debit_account = payment_method_account
                    credit_account = Account.objects.get(id=Account.OTHER_INCOME)
                    entries = [
                        {"account": debit_account, "balance_type": BookEntry.DEBIT},
                        {"account": credit_account, "balance_type": BookEntry.CREDIT},
                    ]
                elif transaction_instance.transaction_type == Transaction.EXPENSE:
                    debit_account = Account.objects.get(id=Account.PERSONAL_EXPENSES)
                    credit_account = payment_method_account
                    entries = [
                        {"account": debit_account, "balance_type": BookEntry.DEBIT},
                        {"account": credit_account, "balance_type": BookEntry.CREDIT},
                    ]
                elif transaction_instance.transaction_type == Transaction.PURCHASE:
                    debit_account = Account.objects.get(id=Account.PURCHASES)
                    credit_account = payment_method_account
                    entries = [
                        {"account": debit_account, "balance_type": BookEntry.DEBIT},
                        {"account": credit_account, "balance_type": BookEntry.CREDIT},
                    ]
                elif transaction_instance.transaction_type == Transaction.SALE:
                    sales_revenue_account = Account.objects.get(id=Account.SALES_REVENUE)
                    sales_cost_account = Account.objects.get(id=Account.SALES_COST)
                    inventory_account = Account.objects.get(id=Account.PURCHASES)
                    entries = [
                        {"account": payment_method_account, "balance_type": BookEntry.DEBIT},
                        {"account": sales_revenue_account, "balance_type": BookEntry.CREDIT},
                        {"account": sales_cost_account, "balance_type": BookEntry.DEBIT},
                        {"account": inventory_account, "balance_type": BookEntry.CREDIT},
                    ]
                else:
                    raise serializers.ValidationError("Invalid transaction type provided.")

            except Account.DoesNotExist as e:
                raise serializers.ValidationError(f"Account does not exist: {str(e)}")

            # Iterate over entries to create BookEntries for each account
            for entry in entries:
                account = entry["account"]
                balance_type = entry["balance_type"]
                user_balance, _ = UserAccountBalance.objects.get_or_create(
                    user=user, account=account
                )
                
                BookEntry.objects.create(
                    transaction=transaction_instance,
                    amount=amount,
                    balance_type=balance_type,
                    account=account,
                    user_account_balance=user_balance,
                )

        return transaction_instance


class UserAccountBalanceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source="user.username")
    account = serializers.ReadOnlyField(source="account.name")

    class Meta:
        model = UserAccountBalance
        fields = ["id", "user", "account", "balance"]


class BookEntrySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = BookEntry
        fields = [
            "id",
            "amount",
            "balance_type",
            "account",
            "transaction",
            "user_account_balance",
        ]


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Account
        fields = ["id", "name", "nature"]

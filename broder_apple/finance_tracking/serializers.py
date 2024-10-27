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
                # Payment method accounts to credit or debit
                if payment_method == "cash":
                    payment_method_account = Account.objects.get(id=Account.CASH)
                elif payment_method == "bank":
                    payment_method_account = Account.objects.get(id=Account.BANK)
                else:
                    raise serializers.ValidationError(
                        "Invalid payment method provided."
                    )

                # Transaction types
                if transaction_instance.transaction_type == Transaction.INCOME:
                    debit_account = payment_method_account
                    credit_account = Account.objects.get(id=Account.OTHER_INCOME)
                elif transaction_instance.transaction_type == Transaction.EXPENSE:
                    debit_account = Account.objects.get(id=Account.PERSONAL_EXPENSES)
                    credit_account = payment_method_account
                elif transaction_instance.transaction_type == Transaction.PURCHASE:
                    debit_account = Account.objects.get(id=Account.PURCHASES)
                    credit_account = payment_method_account
                elif transaction_instance.transaction_type == Transaction.SALE:
                    debit_account = payment_method_account
                    credit_account = Account.objects.get(id=Account.SALES_REVENUE)
                else:
                    raise serializers.ValidationError(
                        "Invalid transaction type provided."
                    )

            except Account.DoesNotExist as e:
                raise serializers.ValidationError(f"Account does not exist: {str(e)}")

            # Get or create UserAccountBalance for debit and credit accounts
            debit_user_balance, _ = UserAccountBalance.objects.get_or_create(
                user=user, account=debit_account
            )
            credit_user_balance, _ = UserAccountBalance.objects.get_or_create(
                user=user, account=credit_account
            )

            # Create debit BookEntry
            BookEntry.objects.create(
                transaction=transaction_instance,
                amount=amount,
                balance_type=BookEntry.DEBIT,
                account=debit_account,
                user_account_balance=debit_user_balance,
            )

            # Create credit BookEntry
            BookEntry.objects.create(
                transaction=transaction_instance,
                amount=amount,
                balance_type=BookEntry.CREDIT,
                account=credit_account,
                user_account_balance=credit_user_balance,
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

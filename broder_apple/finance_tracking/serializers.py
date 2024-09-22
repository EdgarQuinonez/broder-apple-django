from rest_framework import serializers
from finance_tracking.models import Account, BookEntry, Transaction
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    transactions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Transaction.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "transactions"]


class TransactionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        payment_method = validated_data["payment_method"]
        amount = validated_data["amount"]

        if payment_method == Transaction.CASH:
            cash_account = Account.objects.get(name="Cash")
            income_account = Account.objects.get(name="Income")
        elif payment_method == Transaction.BANK:
            bank_account = Account.objects.get(name="Bank")
            income_account = Account.objects.get(name="Income")

        BookEntry.objects.create(
            transaction=transaction,
            amount=amount,
            balance_type=BookEntry.DEBIT,
            account=(
                bank_account if payment_method == Transaction.BANK else cash_account
            ),
        )

        BookEntry.objects.create(
            transaction=transaction,
            amount=amount,
            balance_type=BookEntry.CREDIT,
            account=income_account,
        )

        return transaction


class BookEntrySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = BookEntry
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"

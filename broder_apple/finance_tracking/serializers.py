from rest_framework import serializers
from finance_tracking.models import Account, BookEntry, Transaction
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    transactions = serializers.HyperlinkedRelatedField(
        many=True, view_name="transaction-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["id", "username", "transactions"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    # Password should be write-only and require confirmation
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirm Password",
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")
        extra_kwargs = {
            "email": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        # Remove password2 as it's not needed for user creation
        validated_data.pop("password2")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    id = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        payment_method = validated_data["payment_method"]
        amount = validated_data["amount"]

        if payment_method == Transaction.CASH:
            cash_account = Account.objects.get(name="Efectivo")
            income_account = Account.objects.get(name="Otros Ingresos")
        elif payment_method == Transaction.BANK:
            bank_account = Account.objects.get(name="Banco")
            income_account = Account.objects.get(name="Otros Ingresos")

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


class BookEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BookEntry
        fields = "__all__"


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    id = serializers.ReadOnlyField()
    # url = serializers.HyperlinkedIdentityField(
    #     view_name="account-detail", lookup_field="id"
    # )

    class Meta:
        model = Account
        fields = "__all__"

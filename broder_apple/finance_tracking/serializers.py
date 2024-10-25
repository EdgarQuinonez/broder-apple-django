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
    id = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Transaction
        fields = [
            "id",
            "user",
            "debit_account",
            "credit_account",
            "description",
            "amount",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)

        debit_account = validated_data["debit_account"]
        credit_account = validated_data["credit_account"]

        amount = validated_data["amount"]

        BookEntry.objects.create(
            transaction=transaction,
            amount=amount,
            balance_type=BookEntry.DEBIT,
            account=debit_account,
        )

        BookEntry.objects.create(
            transaction=transaction,
            amount=amount,
            balance_type=BookEntry.CREDIT,
            account=credit_account,
        )

        return transaction


class BookEntrySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = BookEntry
        fields = ["id", "amount", "balance_type", "account", "transaction"]


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Account
        fields = ["id", "name", "nature"]

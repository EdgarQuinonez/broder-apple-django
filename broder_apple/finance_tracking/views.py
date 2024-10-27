from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


from .serializers import (
    AccountSerializer,
    TransactionSerializer,
)
from .models import Transaction, Account
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "transactions": reverse("transaction-list", request=request, format=format),
            "accounts": reverse("account-list", request=request, format=format),
        }
    )


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="income",
    )
    def income(self, request, *args, **kwargs):
        """
        Create an income transaction with double-entry accounting.
        """
        transaction_type = Transaction.INCOME
        amount = request.data.get("amount")
        description = request.data.get("description", "")
        payment_method = request.data.get("payment_method")

        if not amount:
            return Response(
                {"error": "Amount is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        elif not payment_method:
            return Response(
                {"error": "Payment method is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif payment_method not in ["cash", "bank"]:
            return Response(
                {"error": "Invalid payment method."}, status=status.HTTP_400_BAD_REQUEST
            )

        transaction_data = {
            "transaction_type": transaction_type,
            "amount": amount,
            "description": description,
            "payment_method": payment_method,
        }

        serializer = TransactionSerializer(data=transaction_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

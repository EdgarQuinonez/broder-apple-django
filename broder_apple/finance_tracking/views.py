# your_app/views.py

from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from finance_tracking.permissions import IsOwnerOrReadOnly

from .serializers import (
    AccountSerializer,
    TransactionSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)
from .models import Transaction, Account
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "transactions": reverse("transaction-list", request=request, format=format),
            "accounts": reverse("account-list", request=request, format=format),
            "api-token-auth": reverse("api-token-auth", request=request, format=format),
            "token": reverse("token-detail", request=request, format=format),
        }
    )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
        # Extract and validate the payment method
        payment_method = request.data.get("payment_method")
        amount = request.data.get("amount")
        if not amount:
            return Response(
                {"error": "Amount is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Map payment method to debit account (cash or bank)
        try:
            if payment_method == "cash":
                debit_account = Account.objects.get(account_type="cash")
            elif payment_method == "bank":
                debit_account = Account.objects.get(account_type="bank")
            else:
                return Response(
                    {"error": "Invalid payment method."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Define the "other income" credit account
            credit_account = Account.objects.get(account_type="income")
        except Account.DoesNotExist:
            return Response(
                {"error": "Specified account not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create data for the serializer
        transaction_data = {
            "user": request.user.username,
            "debit_account": debit_account.id,
            "credit_account": credit_account.id,
            "amount": amount,
            "description": request.data.get("description", ""),
        }

        # Initialize the serializer with data
        serializer = self.get_serializer(data=transaction_data)
        if serializer.is_valid():
            # Save the transaction and create BookEntries
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CustomObtainAuthToken(ObtainAuthToken):
    """
    Custom view to obtain auth token.
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token_key = response.data.get("token")
        return Response({"token": token_key})


class TokenDetailView(APIView):
    """
    Retrieve the token for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({"token": token.key})


class UserRegistrationView(APIView):
    """
    Register a new user.
    """

    permission_classes = [permissions.AllowAny]  # Allow anyone to access this view

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Automatically create a token for the new user
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"user": UserSerializer(user).data, "token": token.key},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

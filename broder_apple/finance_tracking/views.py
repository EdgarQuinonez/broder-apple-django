from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from inventory_management.models import Inventory, Log


from .serializers import (
    AccountSerializer,
    BookEntrySerializer,
    TransactionSerializer,
    UserAccountBalanceSerializer,
)
from .models import BookEntry, Transaction, Account, UserAccountBalance
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def _create_transaction(self, request, transaction_type):
        description = request.data.get("description", "")
        payment_method = request.data.get("payment_method")
        transaction_data = {
            "transaction_type": transaction_type,
            "description": description,
            "payment_method": payment_method,
        }

        # Handle purchase transaction
        if transaction_type == Transaction.PURCHASE:
            product_log_id = request.data.get("productLogID")
            if not product_log_id:
                return Response(
                    {"error": "Product Log ID is required for purchase transactions."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                product_log = Log.objects.get(id=product_log_id)
                transaction_data["amount"] = product_log.listed_price
                transaction_data["description"] = (
                    f"Compra de {product_log.product.title}"
                )
            except Log.DoesNotExist:
                return Response(
                    {"error": "Invalid Product ID."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Handle sale transaction
        elif transaction_type == Transaction.SALE:
            inventory_id = request.data.get("inventoryID")
            if not inventory_id:
                return Response(
                    {"error": "Inventory ID is required for sale transactions."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                inventory = Inventory.objects.get(id=inventory_id)
                transaction_data["amount"] = request.data.get("sale_price")
                transaction_data["description"] = (
                    f"Venta de {inventory.product.title}"
                )
            except Inventory.DoesNotExist:
                return Response(
                    {"error": "Invalid Inventory ID."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            # For other transactions, retrieve the amount
            amount = request.data.get("amount")
            if not amount:
                return Response(
                    {"error": "Amount is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            transaction_data["amount"] = amount

        # Validate payment_method for all transaction types
        if not payment_method:
            return Response(
                {"error": "Payment method is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif payment_method not in ["cash", "bank"]:
            return Response(
                {"error": "Invalid payment method."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the transaction
        serializer = self.get_serializer(data=transaction_data)
        if serializer.is_valid():
            transaction_instance = serializer.save(user=request.user)
            
            # Transition product lifecycle if applicable
            if transaction_type == Transaction.PURCHASE:
                product_log.product.move_to_inventory(
                    buyout_price=request.data.get("buyout_price"),
                    estimated_sale_price=request.data.get("estimated_sale_price"),
                    seller=request.data.get("seller")
                )
            elif transaction_type == Transaction.SALE:
                inventory.product.move_to_sale(
                    sale_price=request.data.get("sale_price"),
                    buyer=request.data.get("buyer"),
                )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="income",
    )
    def income(self, request, *args, **kwargs):
        """Create an income transaction with double-entry accounting."""
        return self._create_transaction(request, Transaction.INCOME)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="expense",
    )
    def expense(self, request, *args, **kwargs):
        """Create an expense transaction with double-entry accounting."""
        return self._create_transaction(request, Transaction.EXPENSE)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="purchase",
    )
    def purchase(self, request, *args, **kwargs):
        """Create a purchase transaction with double-entry accounting."""
        
        return self._create_transaction(request, Transaction.PURCHASE)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
        url_path="sale",
    )
    def sale(self, request, *args, **kwargs):
        """Create a sale transaction with double-entry accounting."""
        
        return self._create_transaction(request, Transaction.SALE)
    

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class UserAccountBalanceViewSet(viewsets.ModelViewSet):
    queryset = UserAccountBalance.objects.all()
    serializer_class = UserAccountBalanceSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class BookEntryViewSet(viewsets.ModelViewSet):
    queryset = BookEntry.objects.all()
    serializer_class = BookEntrySerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

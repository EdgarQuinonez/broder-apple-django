from rest_framework import status, generics, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from finance_tracking.permissions import IsOwnerOrReadOnly

from .serializers import (
    AccountSerializer,
    TransactionSerializer,
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
        }
    )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def income(self, request, *args, **kwargs):
        """
        Create an income transaction.
        """
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, type=Transaction.INCOME)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

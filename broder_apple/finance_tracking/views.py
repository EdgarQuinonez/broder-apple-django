from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse

from rest_framework import status, mixins, generics, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from finance_tracking.permissions import IsOwnerOrReadOnly

from .serializers import (
    AccountSerializer,
    BookEntrySerializer,
    TransactionSerializer,
    UserSerializer,
)
from .models import Transaction, BookEntry, Account
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionList(
    generics.ListCreateAPIView,
):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TransactionDetail(
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class BookEntryList(generics.ListCreateAPIView):
    queryset = BookEntry.objects.all()
    serializer_class = BookEntrySerializer


class BookEntryDetail(
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = BookEntry.objects.all()
    serializer_class = BookEntrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetail(
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class IncomeTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, type=Transaction.INCOME)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

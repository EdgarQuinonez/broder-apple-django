from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse

from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .serializers import TransactionSerializer
from .models import Transaction, BookEntry, Account


class TransactionList(
    generics.ListCreateAPIView,
):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetail(
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

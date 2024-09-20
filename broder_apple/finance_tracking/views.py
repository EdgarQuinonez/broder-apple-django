from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Transaction, BookEntry, Account
from django.views import generic

# Create your views here.
from django.http import HttpResponse


class IndexView(generic.ListView):
    model = Transaction
    template_name = "finance_tracking/index.html"


class BookEntryView(generic.ListView):
    template_name = "finance_tracking/bookentry.html"
    context_object_name = "latest_bookentry_list"

    def get_queryset(self):
        return BookEntry.objects.order_by("-entry_date")[:5]


class AccountView(generic.ListView):
    template_name = "finance_tracking/account.html"
    context_object_name = "latest_account_list"

    def get_queryset(self):
        return Account.objects.order_by("account_name")

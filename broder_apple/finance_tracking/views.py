from django.shortcuts import render
from .models import Transaction, BookEntry, Account
from django.views import generic

# Create your views here.
from django.http import HttpResponse


class IndexView(generic.ListView):
    template_name = "finance_tracking/index.html"
    context_object_name = "latest_transaction_list"

    def get_queryset(self):
        return Transaction.objects.order_by("-transaction_date")[:5]


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

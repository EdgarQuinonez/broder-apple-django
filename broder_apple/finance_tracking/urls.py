from django.urls import path
from . import views

urlpatterns = [
    path("", views.api_root),
    path("finance_tracking/", views.TransactionList.as_view(), name="transaction-list"),
    path(
        "finance_tracking/<int:pk>/",
        views.TransactionDetail.as_view(),
        name="transaction-detail",
    ),
    path(
        "finance_tracking/income/",
        views.IncomeTransactionView.as_view(),
        name="income-transaction",
    ),
    path("finance_tracking/account/", views.AccountList.as_view(), name="account-list"),
    path(
        "finance_tracking/account/<int:pk>/",
        views.AccountDetail.as_view(),
        name="account-detail",
    ),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
]

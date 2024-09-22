from django.urls import path
from . import views

urlpatterns = [
    path("finance_tracking/", views.TransactionList.as_view()),
    path("finance_tracking/<int:pk>/", views.TransactionDetail.as_view()),
    path(
        "finance_tracking/income/",
        views.IncomeTransactionView.as_view(),
        name="income-transaction",
    ),
    path("finance_tracking/account/", views.AccountList.as_view()),
    path("finance_tracking/account/<int:id>/", views.AccountDetail.as_view()),
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
]

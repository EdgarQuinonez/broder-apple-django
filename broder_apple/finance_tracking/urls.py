from django.urls import path
from . import views

urlpatterns = [
    path("finance_tracking/", views.TransactionList.as_view()),
    path("finance_tracking/<int:pk>/", views.TransactionDetail.as_view()),
]

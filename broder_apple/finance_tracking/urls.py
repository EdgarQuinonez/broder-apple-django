from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bookentry", views.BookEntryView.as_view(), name="bookentry"),
    path("account", views.AccountView.as_view(), name="account"),
]

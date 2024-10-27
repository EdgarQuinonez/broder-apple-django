from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserLoginAPIView, UserViewSet
from .views import UserRegisterAPIView
from .views import UserLogoutAPIView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("register/", UserRegisterAPIView().as_view(), name="user_register"),
    path("logout/", UserLogoutAPIView.as_view(), name="user_logout"),
]

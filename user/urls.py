from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from event.views import EventViewset

from .views import CustomUserViewset, LoginView, LogoutView

router = routers.DefaultRouter()

router.register(r"user", CustomUserViewset)
router.register(r"event", EventViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

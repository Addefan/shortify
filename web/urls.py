from django.urls import path

from web.views import RegisterView, LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

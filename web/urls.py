from django.urls import path

from web.views import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
]

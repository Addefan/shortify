from django.urls import path

from web.views import CreateLinkView, RegisterView, LoginView, LogoutView, ProfileView, LinkView

urlpatterns = [
    path("", CreateLinkView.as_view(), name="main"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("link/<str:short_url>", LinkView.as_view(), name="link"),
]

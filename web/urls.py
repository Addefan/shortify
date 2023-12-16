from django.urls import path

from web.views import CreateLinkView, RegisterView, LoginView, LogoutView, ProfileView, LinkView, LinkPreviewView, \
    LinkListView

urlpatterns = [
    path("", CreateLinkView.as_view(), name="main"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("links/<str:short_url>", LinkView.as_view(), name="link"),
    path("links/<int:id>/preview", LinkPreviewView.as_view(), name="link-preview"),
    path("links/", LinkListView.as_view(), name="link-list"),
]

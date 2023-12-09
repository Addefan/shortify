from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login

from web.forms import RegisterForm, LoginForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "web/register.html"
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = "web/login.html"

    def get_success_url(self):
        return self.request.GET.get("next") or reverse("main")


class LogoutView(SuccessMessageMixin, DjangoLogoutView):
    next_page = reverse_lazy("main")

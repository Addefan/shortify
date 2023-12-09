from django.contrib.auth import login
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from web.forms import RegisterForm
from web.models import User


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "web/register.html"
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class LogoutView(SuccessMessageMixin, DjangoLogoutView):
    next_page = reverse_lazy("main")

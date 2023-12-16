from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.views.generic import CreateView, UpdateView, RedirectView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.http import Http404

from web.forms import RegisterForm, LoginForm, ProfileForm, LinkCreationForm
from web.models import Link


class CreateLinkView(CreateView):
    form_class = LinkCreationForm
    template_name = "web/link-create-form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("link-preview", args=(self.object.id,))


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
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.request.GET.get("next") or reverse("main")


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("main")


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = "web/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user


class LinkView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        link = get_object_or_404(Link, short_relative_url=kwargs["short_url"])

        if not link.is_public and self.request.user != link.user:
            raise Http404

        return link.original_absolute_url


class LinkPreviewView(DetailView):
    model = Link
    pk_url_kwarg = "id"
    context_object_name = "link"
    template_name = "web/link-preview.html"


class LinkListView(LoginRequiredMixin, ListView):
    model = Link
    context_object_name = "links"
    template_name = "web/link-list.html"

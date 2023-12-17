from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, RedirectView, DetailView, ListView, DeleteView
from ipware import get_client_ip

from web.forms import RegisterForm, LoginForm, ProfileForm, LinkCreationForm
from web.models import Link, Visit


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
    def get(self, request, *args, **kwargs):
        link = get_object_or_404(Link, short_relative_url=kwargs["short_url"])
        visit = Visit(link=link)

        if request.user.is_authenticated:
            visit.user = request.user

        visitor_ip, is_routable = get_client_ip(request)
        if visitor_ip and is_routable:
            visit.visitor_ip = visitor_ip

        visit.save()
        return super().get(request, *args, **kwargs)

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

    def get_queryset(self):
        links = Link.objects.select_related("user")

        if not self.request.user.is_superuser:
            return links.filter(user=self.request.user)
        return links.all()


class LinkDeleteView(UserPassesTestMixin, DeleteView):
    model = Link
    pk_url_kwarg = "id"

    def test_func(self):
        return self.request.user == self.get_object().user or self.request.user.is_superuser

    def get_success_url(self):
        return self.request.POST.get("next") or reverse("main")

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Link(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    original_absolute_url = models.URLField(max_length=2048, verbose_name="Сокращаемая ссылка")
    short_relative_url = models.URLField(max_length=128)
    is_public = models.BooleanField(default=True, verbose_name="Открыть доступ к ссылке")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("link", args=(self.short_relative_url,))


class Visit(models.Model):
    link = models.ForeignKey(Link, models.CASCADE)
    visitor_ip = models.GenericIPAddressField()
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    visited_at = models.DateTimeField(auto_now_add=True)

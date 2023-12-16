from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Link(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, verbose_name="Создатель ссылки")
    original_absolute_url = models.URLField(max_length=2048, verbose_name="Ссылка для сокращения")
    short_relative_url = models.URLField(max_length=128, verbose_name="Сокращённая ссылка")
    is_public = models.BooleanField(default=True, verbose_name="Открыть доступ к ссылке")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана в")

    def get_absolute_url(self):
        return reverse("link", args=(self.short_relative_url,))


class Visit(models.Model):
    link = models.ForeignKey(Link, models.CASCADE, verbose_name="Ссылка")
    visitor_ip = models.GenericIPAddressField(verbose_name="IP посетителя")
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True, verbose_name="Посетитель")
    visited_at = models.DateTimeField(auto_now_add=True, verbose_name="Посетил в")

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Link(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    original_absolute_url = models.URLField(max_length=2048)
    short_relative_url = models.CharField(max_length=128)
    is_public = models.BinaryField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Visit(models.Model):
    link = models.ForeignKey(Link, models.CASCADE)
    visitor_ip = models.GenericIPAddressField()
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    visited_at = models.DateTimeField(auto_now_add=True)
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import ModelForm

from web.models import Link
from web.service import generate_short_link


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_suffix = ""
        for visible in self.visible_fields():
            if isinstance(visible.field.widget, forms.CheckboxInput):
                visible.field.widget.attrs["class"] = "form-check-input"
            else:
                visible.field.widget.attrs.update({
                    "class": "form-control",
                    "placeholder": "placeholder"
                })

    def clean(self):
        super().clean()
        for visible in self.visible_fields():
            if visible.name in self._errors:
                visible.field.widget.attrs["class"] += " is-invalid"


class RegisterForm(BootstrapFormMixin, UserCreationForm):
    pass


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    pass


class ProfileForm(BootstrapFormMixin, UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].disabled = True
        self.fields.pop("password", None)

    class Meta(UserChangeForm.Meta):
        fields = ("first_name", "last_name", "email", "username")
        help_texts = {"username": None}


class LinkCreationForm(BootstrapFormMixin, ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if not self.user.is_anonymous:
            self.instance.user = self.user

        short_link = generate_short_link(self.instance.original_absolute_url)
        while Link.objects.filter(short_relative_url=short_link).count():
            short_link = generate_short_link(self.instance.original_absolute_url)
        self.instance.short_relative_url = short_link

        if commit:
            instance.save()

        return instance

    class Meta:
        model = Link
        fields = ("original_absolute_url", "is_public")

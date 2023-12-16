from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


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

from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({
                "class": "form-control",
                "placeholder": "placeholder"
            })

    def clean(self):
        super().clean()
        for visible in self.visible_fields():
            if visible.name in self._errors:
                visible.field.widget.attrs["class"] += " is-invalid"

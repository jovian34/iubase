from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.db import models

def urlfields_assume_https(db_field, **kwargs):
    """
    ModelForm.Meta.formfield_callback function to assume HTTPS for scheme-less
    domains in URLFields.
    """
    if isinstance(db_field, models.URLField):
        kwargs["assume_scheme"] = "https"
    return db_field.formfield(**kwargs)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("x_prof",)
        formfield_callback = urlfields_assume_https

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
        formfield_callback = urlfields_assume_https

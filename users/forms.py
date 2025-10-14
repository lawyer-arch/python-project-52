from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
        )

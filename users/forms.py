from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms


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


class CustomUserChangeForm(forms.ModelForm):
    # Дублируем поля паролей вручную
    password1 = forms.CharField(
        label="Пароль",
        required=False,  # Пароль необязателен
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        required=False,  # Подтверждение тоже необязательно
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз."
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')  # Username убран из обязательных полей

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Чтобы разрешить оставить old username, если не указан new one
        self.fields['username'].required = False

    def clean_password2(self):
        """Проверка совпадения паролей"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 or password2:  # Только если пользователь пытается сменить пароль
            if password1 != password2:
                raise ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        # Устанавливаем пароль, если он был введен
        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])
        # username останется прежним, если новое значение не указано
        if not self.cleaned_data.get('username'):
            user.username = self.instance.username
        if commit:
            user.save()
        return user


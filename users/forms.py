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
    # Поля паролей вручную
    password1 = forms.CharField(
        label="Пароль",
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз."
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 or password2:
            if password1 != password2:
                raise ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        # Установка пароля, если задан новый
        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])

        # Сохранять username, если не указана новая версия
        new_username = self.cleaned_data.get('username')
        if not new_username or new_username.strip() == "":
            user.username = self.instance.username  # Восстанавливаем старое значение
        else:
            user.username = new_username  # Иначе применяем новое значение

        if commit:
            user.save()
        return user


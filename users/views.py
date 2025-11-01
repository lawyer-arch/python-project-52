import logging
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
# from django.urls import reverse_lazy

from .forms import RegisterForm, CustomUserChangeForm

logger = logging.getLogger("users")


class FormLoggerMixin:
    """
    Логирует успешное сохранение формы в классовых представлениях.
    Используется вместе с CreateView/UpdateView/DeleteView.
    """

    log_message: str = "Object saved: {obj}"

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(self.log_message.format(obj=self.object))
        return response


class PermissionMessageMixin:
    permission_denied_message = _("У вас нет прав для выполнения этого действия.")
    redirect_url = "users:users_list"

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.redirect_url)


class UserPermissionTestMixin(UserPassesTestMixin):
    """
    Проверяет, что пользователь изменяет или удаляет только свой профиль,
    либо является суперпользователем.
    """

    def test_func(self):
        user = self.get_object()
        return self.request.user.pk == user.pk or self.request.user.is_superuser


class UsersListView(ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"


class UsersCreateView(FormLoggerMixin, SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = "users/create.html"
    success_url = "/login/"
    success_message = _("Пользователь успешно зарегистрирован!")
    log_message = "Создать пользователя: {obj.username}"

    # код отладки после удалить
    def form_valid(self, form):
        print("Форма валидна, сохраняем объект")  # Отладка
        response = super().form_valid(form)
        print("Перенаправление на:", self.get_success_url())
        return response

    def form_invalid(self, form):
        print("Форма невалидна. Ошибки:", form.errors)  # Отладка
        print("Данные:", form.data)
        return super().form_invalid(form)


class UsersUpdateView(
    PermissionMessageMixin,
    FormLoggerMixin,
    SuccessMessageMixin,
    LoginRequiredMixin,
    UserPermissionTestMixin,
    UpdateView,
):
    model = User
    form_class = CustomUserChangeForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:users_list")
    success_message = _("Профиль успешно обновлен!")
    log_message = "Пользователь обновлен: {obj.username}"


class UsersDeleteView(
    PermissionMessageMixin,
    FormLoggerMixin,
    SuccessMessageMixin,
    LoginRequiredMixin,
    UserPermissionTestMixin,
    DeleteView
):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:users_list")
    success_message = _("Пользователь успешно удален!")
    log_message = "Пользователь удален: {obj.username}"

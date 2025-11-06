import logging
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .forms import RegisterForm, CustomUserChangeForm
from task_manager.tasks.models import Task

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

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
            return redirect("login")
        messages.error(self.request, _("У вас нет прав для изменения другого пользователя."))
        return redirect("users:users_list")


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
    success_message = _("Пользователь успешно зарегистрирован")
    log_message = "Создать пользователя: {obj.username}"


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
    success_message = _("Пользователь успешно изменен")
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

    def post(self, request, *args, **kwargs):
        """
        Переопределяем POST, чтобы перед удалением проверить связанные задачи.
        """
        self.object = self.get_object()  # объект берется по pk из URL
        user_id = self.object.id

        # Проверяем, есть ли задачи, автором которых является пользователь
        if Task.objects.filter(author=self.object).exists():
            messages.error(
                request,
                _("Невозможно удалить пользователя, потому что он используется")
            )
            logger.warning(f"Попытка удалить пользователя {user_id}, который является автором задач")
            return redirect("users:users_list")

        # Если связей нет — вызываем стандартное удаление
        response = super().delete(request, *args, **kwargs)
        messages.success(request, _("Пользователь успешно удален"))
        logger.info(f"Пользователь {user_id} удалён")
        return response

import logging
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy

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


class UsersListView(ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"


class UsersCreateView(FormLoggerMixin, SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = _("Пользователь успешно зарегистрирован!")
    log_message = "Создать пользователя: {obj.username}"


class UsersUpdateView(FormLoggerMixin, SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:users_list")
    success_message = _("Профиль успешно обновлен!")
    log_message = "Пользователь обновлен: {obj.username}"

    def test_func(self):
        return self.request.user.pk == self.get_object().pk or self.request.user.is_superuser


class UsersDeleteView(FormLoggerMixin, SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:users_list")
    success_message = _("Пользователь успешно удален!")
    log_message = "Пользователь удален: {obj.username}"

    def test_func(self):
        return self.request.user.pk == self.get_object().pk or self.request.user.is_superuser

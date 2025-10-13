import logging
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
    )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .forms import RegisterForm, CustomUserChangeForm
from django.urls import reverse_lazy

logger = logging.getLogger('users')

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
    template_name = 'users/list.html'
    context_object_name = 'users'


class UsersCreateView(FormLoggerMixin, SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _("The user has been successfully registered!")
    log_message = "User create: {obj.username}"




class UsersUpdateView(
    FormLoggerMixin,
    SuccessMessageMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
    ):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:users_list')
    success_message = _("Profile successfully updated!")
    log_message = "User updated: {obj.username}"

    def test_func(self):
        return self.request.user.pk == self.get_object().pk or self.request.user.is_superuser
    

class UsersDeleteView(
    FormLoggerMixin,
    SuccessMessageMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
    ):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:users_list')
    success_message = _("The user has been successfully deleted!")
    log_message = "User deleted: {obj.username}"

    def test_func(self):
        return self.request.user.pk == self.get_object().pk or self.request.user.is_superuser

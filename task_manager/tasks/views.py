import logging
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_filters.views import FilterView

from .filters import TaskFilter
from .models import Task
from .forms import TaskForm


logger = logging.getLogger("tasks")


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


# ---------------------------
# Список задач
# ---------------------------
class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


# ---------------------------
# Вывод конкретной задачи
# ---------------------------
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = "task"


# ---------------------------
# Создание задачи
# ---------------------------
class TaskCreateView(LoginRequiredMixin, FormLoggerMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    context_object_name = "task"
    success_url = reverse_lazy("tasks:tasks_list")
    success_message = _("Задача успешно создана")
    log_message = "Создана задача: {obj}"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# ---------------------------
# Редактирование задачи
# ---------------------------
class TaskUpdateView(LoginRequiredMixin, FormLoggerMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    context_object_name = "task"
    success_url = reverse_lazy("tasks:tasks_list")
    success_message = _("Задача успешно изменена")
    log_message = "Изменена задача: {obj}"


# ---------------------------
# Удаление задачи
# ---------------------------
class TaskDeleteView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    context_object_name = "task"
    success_url = reverse_lazy("tasks:tasks_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, _("Невозможно удалить задачу — вы не являетесь ее автором"))
        return redirect('tasks:tasks_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        logger.info(f"Задача удалена: {self.object}")
        messages.success(request, _("Задача успешно удалена"))
        return super().delete(request, *args, **kwargs)

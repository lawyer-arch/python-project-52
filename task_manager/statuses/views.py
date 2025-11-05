import logging
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Status
from task_manager.tasks.models import Task
from .forms import StatusForm

logger = logging.getLogger("statuses")


class FormLoggerMixin:
    """
    Логирует успешное сохранение/изменение объекта в CreateView/UpdateView/DeleteView.
    """

    log_message = "Создан объект: {obj}"

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(self.log_message.format(obj=self.object))
        return response


# ---------------------------
# Список статусов
# ---------------------------
class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/list.html"
    context_object_name = "statuses"


# ---------------------------
# Создание статуса
# ---------------------------
class StatusCreateView(LoginRequiredMixin, FormLoggerMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses:statuses_list")  # Редирект на список после создания
    success_message = _("Статус успешно создан!")
    log_message = "Создан статус: {obj}"


# ---------------------------
# Обновление статуса
# ---------------------------
class StatusUpdateView(LoginRequiredMixin, FormLoggerMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm  # Обязательный параметр для UpdateView
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses:statuses_list")  # Редирект на список после обновления
    success_message = _("Статус успешно изменен")
    log_message = "Статус обновлён: {obj}"


# ---------------------------
# Удаление статуса
# ---------------------------
class StatusDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:statuses_list")
    success_message = _("Статус успешно удален")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        status_id = self.object.id

        if Task.objects.filter(status=self.object).exists():
            messages.error(
                request,
                _("Невозможно удалить статус, потому что он используется")
            )
            logger.warning(f"Попытка удалить статус {status_id}, который используется")
            return redirect("statuses:statuses_list")

        response = super().delete(request, *args, **kwargs)
        messages.success(request, self.success_message)
        logger.info(f"Статус {status_id} удален")
        return response

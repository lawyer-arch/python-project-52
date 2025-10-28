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
    success_message = _("Статус успешно изменён!")
    log_message = "Статус обновлён: {obj}"


# ---------------------------
# Удаление статуса
# ---------------------------
class StatusDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:statuses_list")

    def post(self, request, *args, **kwargs):
        """
        Логирование удаления и проверка связанных задач.
        Если объект используется в задачах, удаление запрещено.
        """
        self.object = self.get_object()

        # Проверяем наличие связанных задач ДО запуска стандартного удаления
        if self.object.task_set.exists():
            messages.error(request, _("Невозможно удалить статус, он используется задачами!"))
            return redirect(self.success_url)

        # Если задач нет, продолжаем удаление
        try:
            # Удаляем объект вручную
            self.object.delete()
            logger.info(f"Статус удалён: {self.object}")
            messages.success(request, _("Статус успешно удалён!"))
        except ObjectDoesNotExist:
            # Объект уже удалён кем-то другим
            messages.warning(request, _("Объект уже удалён."))
        except Exception as e:
            # Обработка любых неожиданных ошибок
            messages.error(request, f"{_('Возникла ошибка при удалении')}: {str(e)}")

        return redirect(self.success_url)

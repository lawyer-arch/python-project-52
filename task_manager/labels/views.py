import logging
from django.shortcuts import redirect
from django.views.generic import(
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView

from .models import Label
from task_manager.tasks.models import Task


logger = logging.getLogger("labels")


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
# Список меток
# ---------------------------
class LabelsListView(LoginRequiredMixin, FilterView, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = "labels"


# ---------------------------
# Вывод конкретной метки
# ---------------------------
class LabelDetailView(LoginRequiredMixin, DetailView):
    model = Label
    template_name = 'labels/detail.html'
    context_object_name = "labels"


# ---------------------------
# Создание метки
# ---------------------------
class LabelCreateView(
    LoginRequiredMixin,
    FormLoggerMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Label
    template_name = 'labels/create.html'
    context_object_name = "label"
    fields = ['name']
    success_url = reverse_lazy("labels:labels_list")
    success_message = _("Метка успешно создана")
    log_message = "Создана метка: {obj}"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# ---------------------------
# Редактирование метки
# ---------------------------
class LabelUpdateView(
    LoginRequiredMixin,
    FormLoggerMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Label
    template_name = 'labels/update.html'
    context_object_name = "label"
    fields = ['name']
    success_url = reverse_lazy("labels:labels_list")
    success_message = _("Метка успешно изменена")
    log_message = "Изменена метка: {obj}"


# ---------------------------
# Удаление метки
# ---------------------------
class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    context_object_name = "label"
    success_url = reverse_lazy("labels:labels_list")

    def post(self, request, *args, **kwargs):
        """
        Переопределяем POST, 
        чтобы перед удалением проверить связанные задачи.
        """
        self.object = self.get_object()
        label_id = self.object.id

        # Проверяем, есть ли задачи с этой меткой
        if Task.objects.filter(labels=self.object).exists():
            messages.error(
                request,
                "Невозможно удалить метку, " \
                "потому что она используется в задачах"
            )
            logger.warning(
                f"Попытка удалить метку {label_id}, связанную с задачами"
            )
            return redirect(self.success_url)

        # Если связей нет — вызываем стандартное удаление
        response = super().post(request, *args, **kwargs)
        messages.success(request, "Метка успешно удалена")
        logger.info(f"Метка {label_id} удалена")
        return response

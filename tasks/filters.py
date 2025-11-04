
import django_filters
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Task
from statuses.models import Status
from labels.models import Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Исполнитель",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    label = django_filters.ModelMultipleChoiceFilter(
        field_name='labels',  # Связанное поле ManyToManyField
        queryset=Label.objects.all(),
        label="Метка",
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),  # Возможность выбора нескольких меток
        conjoined=True,  # Выбор хотя бы одной метки из множества (AND логика)
    )

    own_task = django_filters.BooleanFilter(
        label=_('Только свои задачи'),
        method='own_tasks_filter',
        widget=forms.CheckboxInput()
    )

    def own_tasks_filter(self, queryset, name, value):
        """
        Фильтрует задачи, принадлежащие текущему пользователю (если value == True).
        """
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label','own_task']

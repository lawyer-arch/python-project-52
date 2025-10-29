
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
        empty_label="---------"
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        empty_label="---------",
        label="Исполнители",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        empty_label="---------",
        label="Метки"
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

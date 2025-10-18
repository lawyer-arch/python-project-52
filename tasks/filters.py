# import django_filters
# from django import forms
# from django.utils.translation import gettext_lazy as _
# from .models import Task
# from labels.models import Label

# class TaskFilter(django_filters.FilterSet):
#     labels = django_filters.ModelChoiceFilter(
#         label=_('Label'),
#         queryset=Label.objects.all()
#     )

#     def own_tasks_filter(self, queryset, value):
#         current_user = self.request.user
#         if value:
#             return queryset.filter(creator=current_user)
#         return queryset

#     own_task = django_filters.BooleanFilter(
#         label=_('My tasks only'),
#         method='own_tasks_filter',
#         widget=forms.CheckboxInput()
#     )

#     class Meta:
#         model = Task
#         fields = ['status', 'executor', 'labels', 'own_task']
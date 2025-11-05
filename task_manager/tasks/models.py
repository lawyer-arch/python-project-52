from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(_("Имя"), max_length=50)
    description = models.TextField(_("Описание"))
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks_authored',
        blank=False,
        null=False,
        verbose_name=_("Автор")
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Исполнитель"),
        related_name='tasks_executed'
    )
    status = models.ForeignKey(
        'statuses.Status',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name=_("Статус"),
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='tasks',
        verbose_name=_("Метки"),
    )

    created_at = models.DateTimeField(verbose_name=_("Дата создания"), auto_now_add=True)

    def __str__(self):
        return self.name

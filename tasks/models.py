from django.db import models
from django.contrib.auth.models import User
from labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks_authored',
        blank=False,
        null=False
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='tasks_executed'
    )
    status = models.ForeignKey(
        'statuses.Status',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='tasks'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

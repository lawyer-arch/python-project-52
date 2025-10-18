from django.db import models
from django.contrib.auth.models import User
from statuses.models import Status

# Модель задачи
class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks_authored'  # авторские задачи
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks_executed'  # задачи, которые выполняет
    )
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
#    labels = models.ManyToManyField(Label, blank=True,
 #                                   verbose_name=_('Labels'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
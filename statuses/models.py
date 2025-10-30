from django.db import models
from django.utils.translation import gettext_lazy as _

# Создаем модель Status
class Status(models.Model):
    name = models.CharField(_("Имя"), max_length=100)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    def __str__(self):
        return self.name

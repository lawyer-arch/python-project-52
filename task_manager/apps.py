# core/apps.py для отладки потом удалить

from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager'

    def ready(self):
        import task_manager.signals  # Регистрирует обработчики сигналов
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

@pytest.fixture
def user(db):
    return User.objects.create_user(username="user1", password="Password123")

@pytest.fixture
def status(db):
    return Status.objects.create(name="Новый")

@pytest.fixture
def task(db, user, status):
    return Task.objects.create(
        name="Старое имя",
        description="Описание",
        author=user,
        status=status
    )

@pytest.fixture
def client_logged(client, user):
    client.login(username=user.username, password="Password123")
    return client


@pytest.mark.django_db
class TestTaskCRUD:

    def test_list_requires_login(self, client):
        url = reverse("tasks:tasks_list")
        response = client.get(url)
        assert response.status_code == 302

    def test_list_view_logged_tasks(self, client_logged):
        url = reverse("tasks:tasks_list")
        response = client_logged.get(url)
        assert response.status_code == 200
        assert "Задачи" in response.content.decode()

    def test_create_task(self, client_logged, user, status):
        url = reverse("tasks:tasks_create")
        response = client_logged.post(
            url,
            {
                "name": "Выполнить",
                "description": "Описание задачи",
                "status": status.pk,
                "executor": user.pk
            },
            follow=True
        )
        assert response.status_code == 200
        task = Task.objects.get(name="Выполнить")
        assert task.author == user

        messages = list(get_messages(response.wsgi_request))
        assert any("Задача успешно создана" in str(m) for m in messages)

    def test_update_task(self, client_logged, task, status):
        url = reverse("tasks:tasks_update", args=[task.pk])
        response = client_logged.post(
            url,
            {
                "name": "Новое имя",
                "description": task.description,
                "status": status.pk,
                "executor": task.executor.pk if task.executor else ""
            },
            follow=True
        )
        task.refresh_from_db()
        assert task.name == "Новое имя"

        messages = list(get_messages(response.wsgi_request))
        assert any("Задача успешно изменена" in str(m) for m in messages)

    def test_delete_task(self, client_logged, task):
        url = reverse("tasks:tasks_delete", args=[task.pk])
        response = client_logged.post(url, follow=True)
        assert response.status_code == 200
        assert not Task.objects.filter(pk=task.pk).exists()


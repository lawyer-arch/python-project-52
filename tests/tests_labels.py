import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="user1",
        password="Password123"
    )


@pytest.fixture
def status(db):
    return Status.objects.create(name="Новый")


@pytest.fixture
def task(db, user, status):
    return Task.objects.create(
        name="Задача 1",
        description="Описание задачи",
        author=user,
        status=status
    )


@pytest.fixture
def label(db):
    return Label.objects.create(name="Важная")


@pytest.fixture
def client_logged(client, user):
    client.login(
        username=user.username,
        password="Password123"
        )
    return client


@pytest.mark.django_db
class TestLabelCRUD:

    def test_list_requires_login(self, client):
        url = reverse("labels:labels_list")
        response = client.get(url)
        assert response.status_code == 302

    def test_list_view_logged_labels(self, client_logged):
        url = reverse("labels:labels_list")
        response = client_logged.get(url)
        assert response.status_code == 200
        assert "Метки" in response.content.decode()

    def test_create_label(self, client_logged):
        url = reverse("labels:labels_create")
        response = client_logged.post(
            url,
            {
                "name": "Новая метка"
            },
            follow=True
        )
        assert response.status_code == 200
        messages = list(get_messages(response.wsgi_request))
        assert any("Метка успешно создана" in str(m) for m in messages)

    def test_update_label(self, client_logged, label):
        url = reverse("labels:labels_update", args=[label.pk])
        response = client_logged.post(
            url,
            {
                "name": "Обновленная метка"
            },
            follow=True
        )
        label.refresh_from_db()
        assert label.name == "Обновленная метка"

        messages = list(get_messages(response.wsgi_request))
        assert any("Метка успешно изменена" in str(m) for m in messages)

    def test_delete_label_without_tasks(self, client_logged, label):
        url = reverse("labels:labels_delete", args=[label.pk])
        response = client_logged.post(url, follow=True)
        assert response.status_code == 200
        assert not Label.objects.filter(pk=label.pk).exists()

    def test_delete_label_with_tasks(self, client_logged, label, task):
        label.tasks.add(task)
        url = reverse("labels:labels_delete", args=[label.pk])
        response = client_logged.post(url, follow=True)

        assert response.status_code == 200
        messages = list(get_messages(response.wsgi_request))

        # Проверяем, что появилось предупреждение о невозможности удаления
        assert any(
            "Невозможно удалить метку, потому что она используется в задачах"
            in str(m) for m in messages
        )

        # Метка не должна удаляться
        assert Label.objects.filter(pk=label.pk).exists()



    def test_detail_label(self, client_logged, label):
        url = reverse("labels:labels_detail", args=[label.pk])
        response = client_logged.get(url)
        assert response.status_code == 200
        assert label.name in response.context['labels'].name
        assert (
            response.context['labels'].created_at.date() == 
            label.created_at.date()
        )

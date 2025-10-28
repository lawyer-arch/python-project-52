import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from tasks.models import Task
from labels.models import Label

@pytest.fixture
def user(db):
    return User.objects.create_user(username="user1", password="Password123")

@pytest.fixture
def task(db, user):
    return Task.objects.create(
        title="Задача 1",
        description="Описание задачи"
    )

@pytest.fixture
def label(db):
    return Label.objects.create(name="Важная")

@pytest.fixture
def client_logged(client, user):
    client.login(username=user.username, password="Password123")
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
        label = Label.objects.get(name="Новая метка")

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
        assert Label.objects.filter(pk=label.pk).exists()

        messages = list(get_messages(response.wsgi_request))
        assert any("Невозможно удалить метку" in str(m) for m in messages)

    def test_detail_label(self, client_logged, label):
        url = reverse("labels:labels_detail", args=[label.pk])
        response = client_logged.get(url)
        assert response.status_code == 200
        assert label.name in response.content.decode()
        assert str(label.created_at.date()) in response.content.decode()

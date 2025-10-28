import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from statuses.models import Status


@pytest.mark.django_db
class TestStatusCRUD:
    #  Создаёт тестового пользователя.
    @pytest.fixture
    def user(self):
        return User.objects.create_user(username="testuser", password="password123")

    #  Логинит тестового пользователя в Django-тестовом клиенте.
    @pytest.fixture
    def client_logged(self, client, user):
        client.login(username="testuser", password="password123")
        return client

    #  Проверяет, что неавторизованный пользователь не может просматривать список статусов.
    def test_list_requires_login(self, client):
        url = reverse("statuses:statuses_list")
        response = client.get(url)
        assert response.status_code == 302  # редирект на логин

    #  Проверяет, что авторизованный пользователь получает страницу со списком статусов.
    def test_list_view_logged_user(self, client_logged):
        url = reverse("statuses:statuses_list")
        response = client_logged.get(url)
        assert response.status_code == 200
        assert "Статусы" in response.content.decode()

    #  Проверяет создание нового статуса и вывод success_message.
    def test_create_status(self, client_logged):
        url = reverse("statuses:statuses_create")
        response = client_logged.post(url, {"name": "В работе"}, follow=True)
        assert response.status_code == 200
        assert Status.objects.filter(name="В работе").exists()

        #  Проверка сообщения после создания
        messages = list(get_messages(response.wsgi_request))
        assert any("Статус успешно создан" in str(m) for m in messages)

    #  Проверяет обновление существующего статуса и вывод success_message.
    def test_update_status(self, client_logged):
        status = Status.objects.create(name="Старое имя")
        url = reverse("statuses:statuses_update", args=[status.pk])
        response = client_logged.post(url, {"name": "Новое имя"}, follow=True)
        assert response.status_code == 200
        status.refresh_from_db()
        assert status.name == "Новое имя"

        #  Проверка сообщения после обновления
        messages = list(get_messages(response.wsgi_request))
        assert any("Статус успешно изменён" in str(m) for m in messages)

    #  Проверяет удаление статуса и вывод success_message.
    def test_delete_status(self, client_logged):
        status = Status.objects.create(name="Удаляемый")
        url = reverse("statuses:statuses_delete", args=[status.pk])
        response = client_logged.post(url, follow=True)
        assert response.status_code == 200
        assert not Status.objects.filter(pk=status.pk).exists()


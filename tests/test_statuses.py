import pytest
from django.urls import reverse
from django.contrib.auth.models import User
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
        url = reverse("statuses_list")
        response = client.get(url)
        assert response.status_code == 302  # редирект на логин

    #  Проверяет, что авторизованный пользователь получает страницу со списком статусов.
    def test_list_view_logged_user(self, client_logged):
        url = reverse("statuses_list")
        response = client_logged.get(url)
        assert response.status_code == 200
        assert "Статусы" in response.content.decode()

    #  Проверяет создание нового статуса.
    def test_create_status(self, client_logged):
        url = reverse("statuses_create")
        response = client_logged.post(url, {"name": "В работе"}, follow=True)
        assert response.status_code == 200
        assert Status.objects.filter(name="В работе").exists()
        assert "Статус успешно создан" in response.content.decode()

    #  Проверяет обновление существующего статуса.
    def test_update_status(self, client_logged):
        status = Status.objects.create(name="Старое имя")
        url = reverse("statuses_update", args=[status.pk])
        response = client_logged.post(url, {"name": "Новое имя"}, follow=True)
        assert response.status_code == 200
        status.refresh_from_db()
        assert status.name == "Новое имя"
        assert "Статус успешно изменён" in response.content.decode()

    # Проверяет удаление статуса.
    def test_delete_status(self, client_logged):
        status = Status.objects.create(name="Удаляемый")
        url = reverse("statuses_delete", args=[status.pk])
        response = client_logged.post(url, follow=True)
        assert response.status_code == 200
        assert not Status.objects.filter(pk=status.pk).exists()
        assert "Статус успешно удалён" in response.content.decode()

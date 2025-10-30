# tests/conftest.py
import pytest
from django.conf import settings
from django.test.client import Client
from users.models import User

# Автоматически задаём SECRET_KEY для всех тестов
@pytest.fixture(autouse=True)
def set_secret_key():
    settings.SECRET_KEY = 'django-insecure-test-key'

# Клиент Django для запросов
@pytest.fixture
def client():
    return Client()

# Простейший пользователь для логина
@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')

# Клиент с залогиненным пользователем
@pytest.fixture
def client_logged(client, user):
    client.login(username='testuser', password='password')
    return client


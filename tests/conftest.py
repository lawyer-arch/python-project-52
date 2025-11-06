# tests/conftest.py
import pytest
from django.conf import settings


# Автоматически задаём SECRET_KEY для всех тестов
@pytest.fixture(autouse=True)
def set_secret_key():
    settings.SECRET_KEY = 'django-insecure-test-key'



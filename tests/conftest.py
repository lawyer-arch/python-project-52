import pytest
from django.conf import settings

@pytest.fixture(autouse=True)
def set_secret_key():
    settings.SECRET_KEY = 'django-insecure-test-key'

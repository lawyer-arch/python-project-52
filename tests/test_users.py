import pytest
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from users.forms import RegisterForm, CustomUserChangeForm

# -------------------------
#  Тесты на основе TestCase
# -------------------------
class UsersViewsTest(TestCase):
    #  Создание тестового пользователя в базе данных и вход в систему под его именем
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123", first_name="Test", last_name="User"
        )
        self.client.login(username="testuser", password="password123")

    #  Проверяем работу представления (view) для списка пользователей
    def test_users_list_view(self):
        url = reverse("users:users_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/list.html")
        self.assertIn(self.user, response.context["users"])

    #  Проверяем работу GET-запроса к странице создания нового пользователя.
    def test_users_create_view_get(self):
        url = reverse("users:users_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/create.html")

    #  Проверяем работу регистрации через POST-запрос
    def test_users_create_view_post(self):
        self.client.logout()
        url = reverse("users:users_create")
        data = {
            "first_name": "New",
            "last_name": "User",
            "username": "newuser",
            "password1": "newpassword123",
            "password2": "newpassword123",
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    #  Защита от несанкционированного доступа к профилям других пользователей
    def test_users_update_view_forbidden(self):
        other_user = User.objects.create_user(username="other", password="pass")
        self.client.force_login(self.user)
        url = reverse("users:users_update", args=[other_user.pk])
        response = self.client.get(url)
        self.assertRedirects(response, reverse("users:users_list"))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("нет прав" in str(m).lower() for m in messages))

    #  Проверяем корректность работы view для удаления пользователя
    def test_users_delete_view_allowed(self):
        url = reverse("users:users_delete", args=[self.user.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("users:users_list"))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    #  Защита от несанкционированного доступа к профилям других пользователей
    def test_users_delete_view_forbidden(self):
        other_user = User.objects.create_user(username="other", password="pass")
        self.client.force_login(self.user)
        url = reverse("users:users_delete", args=[other_user.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("users:users_list"))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("нет прав" in str(m).lower() for m in messages))

    #  Базовая функциональность страницы входа и корректность отображения формы авторизации
    def test_login_view(self):
        self.client.logout()
        url = reverse("login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    #  Проверяем корректность работы выхода из системы
    def test_logout_view(self):
        url = reverse("logout")
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, "/")

    #  Проверяем корректную работу регистрации и вывод success_message
    def test_users_create_view_post_success_message(self):
        self.client.logout()
        url = reverse("users:users_create")
        data = {
            "first_name": "New",
            "last_name": "User",
            "username": "newuser",
            "password1": "newpassword123",
            "password2": "newpassword123",
        }
        response = self.client.post(url, data, follow=True)

        # Добавляем проверки
        # 1. Статус код ответа
        self.assertEqual(response.status_code, 200)
        # 2. Проверка создания пользователя в базе
        self.assertTrue(User.objects.filter(username="newuser").exists())
        # 3. Проверка сообщения об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Пользователь успешно зарегистрирован!")
        # 4. Проверка авторизации
        user = User.objects.get(username="newuser")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "newuser")

    #  Проверяем корректную работу удаления пользователя и вывод success_message
    def test_users_delete_view_success_message(self):
        url = reverse("users:users_delete", args=[self.user.pk])
        response = self.client.post(url, follow=True)
        messages = list(get_messages(response.wsgi_request))
        #  Проверяем наличие сообщения об успешном удалении
        assert any("удален" in str(m).lower() for m in messages)


# --------------------------
#  Тесты форм регистрации и изменения пользователя
# --------------------------
class RegisterFormTest(TestCase):
    def test_valid_registration(self):
        data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "username": "ivanov",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, "Иван")
        self.assertEqual(user.last_name, "Иванов")
        self.assertEqual(user.username, "ivanov")

    def test_invalid_password(self):
        data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "username": "ivanov",
            "password1": "password",
            "password2": "differentpassword",
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_required_fields(self):
        data = {}
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password1", form.errors)
        self.assertIn("password2", form.errors)

class CustomUserChangeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", first_name="Тестовый", last_name="Пользователь", password="testpass123"
        )

    def test_password_field_presence(self):
        # Теперь проверим, что поля пароля включены в форму
        form = CustomUserChangeForm(instance=self.user)
        self.assertIn("password1", form.fields.keys())  # Поля пароля должны присутствовать
        self.assertIn("password2", form.fields.keys())


# -------------------------
#  Проверка логирования с pytest
# -------------------------
@pytest.mark.django_db
def test_user_create_logging(client, caplog):
    url = reverse("users:users_create")
    data = {
        "username": "loguser",
        "first_name": "Log",
        "last_name": "User",
        "password1": "ComplexPass123!",
        "password2": "ComplexPass123!",
    }
    with caplog.at_level("INFO", logger="users"):
        response = client.post(url, data)
        assert "Создать пользователя: loguser" in caplog.text
        assert response.status_code == 302

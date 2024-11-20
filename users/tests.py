from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from users.models import User


class CreateSuperUserCommandTest(TestCase):
    """Тесты для команды создания суперпользователя."""

    def test_create_superuser(self):
        """Тестирование создания суперпользователя через команду."""
        self.assertEqual(User.objects.count(), 0)

        #     # Вызов команды создания суперпользователя
        call_command("csu")

        # Проверка, что пользователь был создан
        user = User.objects.get(phone=80297777777)
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password("admin"))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)

        self.assertEqual(User.objects.count(), 1)


class UserTestCase(TestCase):
    """Тесты для модели пользователя и связанных представлений."""

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом.."""
        self.user = User.objects.create(
            phone=80297777777,
            email="test@tesov.com",
            password="test",
            # token=generate_unique_token(),
        )

    def test_register_view(self):
        """Тестирование регистрации пользователя."""
        url = reverse("users:register")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "neas1dder@gmail.com",
            "phone": "2913152311",
            "password1": "54321qQ!",
            "password2": "54321qQ!",
        }
        self.assertEqual(User.objects.count(), 1)

        response = self.client.post(url, data)

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(User.objects.last().email, "neas1dder@gmail.com")
        self.assertTrue(User.objects.last().first_name, "John")

    def test_profile_view(self):
        """Тестирование профиля пользователя."""
        self.client.force_login(self.user)
        url = reverse("users:profile")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "testuser@example.com",
            "phone": "80297777777",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()

        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "testuser@example.com")

    def test_author_list_view(self):
        """Тестирование списка авторов."""
        User.objects.create(
            phone=802977777717,
            password="test",
            email="test@tesov.ru",
        )
        url = reverse("users:authors")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(User.objects.last().phone, "802977777717")

from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from post.models import Post, Subscription
from post.services import SubscriptionService
from users.models import User


class PostTestCase(TestCase):
    """Тесты для проверки функционала связанного с постами."""

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом.."""
        self.user = User.objects.create(
            phone=80297777777,
            password="test",
        )
        self.post = Post.objects.create(
            author=self.user,
            title="Test title",
            description="Test description",
        )
        self.client.force_login(self.user)

    def test_index_view(self):
        """Тестирование контроллера Indexview."""
        url = reverse("post:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post/base.html")

    def test_post_create(self):
        """Тестирование контроллер PostCreateView для авторизованного пользователя."""
        url = reverse("post:post-create")
        data = {
            "title": "Test",
            "description": "Description",
        }
        response = self.client.post(url, data)

        # Проверяем, что редирект происходит на страницу входа
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.last().title, "Test")
        self.assertEqual(Post.objects.last().description, "Description")
        self.assertEqual(Post.objects.last().author, self.user)

    # вопрос наставнику нужно или нет
    def test_post_create_view_without_login(self):
        """Тестирование контроллер PostCreateView для неавторизованного пользователя."""
        self.client.logout()
        url = reverse("post:post-create")
        data = {
            "title": "Test",
            "description": "Description",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/users/login/")

    def test_post_update(self):
        """Тестирование контроллер PostUpdateView для авторизованного пользователя."""
        url = reverse("post:post-update", args=(self.post.pk,))
        data = {
            "title": "New Test",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.title, "New Test")

    def test_post_delete(self):
        """Тестирование контроллер PostDeleteView для авторизованного пользователя."""
        url = reverse("post:post-delete", args=(self.post.pk,))
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_list(self):
        """Тестирование контроллер PostListView для авторизованного пользователя."""
        url = reverse("post:post-list")
        post1 = Post.objects.create(title="1Post 1", author=self.user)
        post2 = Post.objects.create(title="3Post 2", author=self.user)
        post3 = Post.objects.create(title="2Post 3", author=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 4)
        self.assertEqual(response.context["post_list"][0], post1)
        self.assertEqual(response.context["post_list"][2], post2)
        self.assertEqual(response.context["post_list"][1], post3)
        titles = [post.title for post in response.context["post_list"]]
        self.assertEqual(titles, ["1Post 1", "2Post 3", "3Post 2", "Test title"])


class ChooseSubViewTestCase(TestCase):
    """Тесты для проверки функционала связанного с выбором подписки."""

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом.."""
        self.user = User.objects.create(
            phone=80297777777,
            email="test@tesov.com",
            password="test",
        )
        self.client.force_login(self.user)

    def test_post_new_subscription(self):
        """Тестирование создания новой подписки."""
        url = reverse("post:subscription")
        data = {"type_of_sub": "one_month"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Subscription.objects.last().type_of_sub, "one_month")

    def test_buy_sub_with_active_subscription(self):
        """Тестирование попытки создания подписки при наличии активной."""
        url = reverse("post:subscription")
        Subscription.objects.create(
            user=self.user,
            type_of_sub="three_month",
            is_active=True,
            is_paid=True,
        )
        data = {
            "type_of_sub": "one_month",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)

    def test_choose_sub_unauthorized(self):
        """Тестирование доступа к подписке для неавторизованного пользователя."""
        self.client.logout()
        url = reverse("post:subscription")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)


class PaymentViewTests(TestCase):
    """Тесты для проверки функционала связанного с оплатой."""

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом.."""
        self.user = User.objects.create(
            phone=80297777777,
            email="test@tesov.com",
            password="test",
        )
        self.client.force_login(self.user)
        self.subscription = Subscription.objects.create(
            user=self.user, type_of_sub="one_month", is_paid=False
        )

    # Изолирование тестового кода от реальных функций Stripe API
    @patch("post.views.create_stripe_session")
    @patch("post.views.get_stripe_price")
    def test_get_payment_view(self, mock_get_stripe_price, mock_create_stripe_session):
        """Тестирование GET-запроса страницы оплаты подписки."""
        # Создание объектов, которые будут использоваться вместо оригинальных функций в тесте
        mock_get_stripe_price.return_value = {"id": "price_123", "amount": 1000}
        mock_create_stripe_session.return_value = ("session_id", "payment_link")
        url = reverse("post:subscription-payment", args=(self.subscription.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post/payment.html")
        self.subscription.refresh_from_db()
        self.assertTrue(self.subscription.is_paid)
        self.assertTrue(self.subscription.is_active)
        self.assertIn("subscription", response.context)


class SubConfirmSuccessViewTests(TestCase):
    """Тесты для проверки представления успешного подтверждения подписки."""

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом.."""
        self.user = User.objects.create(
            phone=80297777777,
            password="test",
        )
        self.client.force_login(self.user)

    def test_get_view(self):
        """Тестирование GET-запроса страницы успешного подтверждения."""
        response = self.client.get(reverse("post:sub-success"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post/confirm_success.html")


class SubscriptionServiceTests(TestCase):
    """Тесты для проверки сервисных методов работы с подписками."""

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом.."""
        self.user = User.objects.create(
            phone=80297777777,
            email="test@testov.com",
            password="test",
        )

    def test_get_subscription_interval(self):
        """Тестирование метода получения интервала подписки."""
        # Проверяем, что метод возвращает правильные значения
        self.assertEqual(SubscriptionService.get_subscription_interval("one_month"), 1)
        self.assertEqual(
            SubscriptionService.get_subscription_interval("three_month"), 3
        )
        self.assertEqual(SubscriptionService.get_subscription_interval("six_month"), 6)
        self.assertEqual(SubscriptionService.get_subscription_interval("one_year"), 12)

        # Возвращает None для неверного типа подписки
        self.assertIsNone(SubscriptionService.get_subscription_interval("two_month"))

    def test_has_active_subscription(self):
        """Тестирование метода проверки наличия активной подписки."""
        # Создаем активную подписку
        Subscription.objects.create(user=self.user, is_active=True, is_paid=True)
        self.assertTrue(SubscriptionService.has_active_subscription(self.user))

        # Создаем подписку, которая не оплачена
        Subscription.objects.create(user=self.user, is_active=True, is_paid=False)
        self.assertTrue(SubscriptionService.has_active_subscription(self.user))

        # Проверяем, что метод не выдает подписку при регистрации
        new_user = User.objects.create(
            phone="New Test", email="newtest@testov.com", password="test"
        )
        self.assertFalse(SubscriptionService.has_active_subscription(new_user))

    def test_create_or_update_subscription(self):
        "Тестирование метода создания или обновления подписки."
        subscription = SubscriptionService.create_or_update_subscription(
            self.user, "one_month"
        )
        self.assertEqual(subscription.type_of_sub, "one_month")
        self.assertFalse(subscription.is_paid)

        # Обновляем подписку
        updated_subscription = SubscriptionService.create_or_update_subscription(
            self.user, "three_month"
        )
        self.assertEqual(updated_subscription.type_of_sub, "three_month")

        # Проверяем, что это та же подписка
        self.assertEqual(subscription.id, updated_subscription.id)

        # Проверяем, что подписка не была оплачена
        self.assertFalse(updated_subscription.is_paid)

        # Проверяем, что метод возвращает ту же подписку, если она уже существует
        self.assertEqual(subscription, updated_subscription)

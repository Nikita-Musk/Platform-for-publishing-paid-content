import stripe

from config.settings import STRIPE_API_KEY
from post.models import Subscription

stripe.api_key = STRIPE_API_KEY


def get_stripe_price(amount, interval):
    """Создает цену в stripe."""
    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        recurring={"interval": "month", "interval_count": interval},
        product_data={"name": "Subscription"},
    )


def create_stripe_session(price):
    """Создает сессию на оплату в stripe."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/subscription/success/",  # Сделать шаблон спазипо за пподписку
        # cancel_url='http://127.0.0.1:8000/',
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="subscription",
    )
    return session.get("id"), session.get("url")


class SubscriptionService:

    @staticmethod
    def get_subscription_interval(type_of_sub):
        """Определяет продолжительность выбранной подписки."""
        if type_of_sub == "one_month":
            return 1
        if type_of_sub == "three_month":
            return 3
        if type_of_sub == "six_month":
            return 6
        if type_of_sub == "one_year":
            return 12

    @staticmethod
    def has_active_subscription(user):
        """Проверяет, есть ли у пользователя активная подписка."""
        return Subscription.objects.filter(
            user=user, is_active=True, is_paid=True
        ).exists()

    @staticmethod
    def create_or_update_subscription(user, type_of_sub):
        """Создает подписку для пользователя в состоянии is_paid=False."""
        subscription, created = Subscription.objects.get_or_create(
            user=user, is_paid=False, defaults={"type_of_sub": type_of_sub}
        )

        # Если подписка уже существует, обновляем тип подписки
        if not created:
            subscription.type_of_sub = type_of_sub
            subscription.save()

        return subscription

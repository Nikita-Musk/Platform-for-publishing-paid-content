from post.models import Subscription


def sub_status(request):
    """Добавляем статус подписки на все шаблоны."""
    if request.user.is_authenticated:
        # Получаем последнюю активную подписку пользователя
        subscription = Subscription.objects.filter(
            user=request.user, is_active=True
        ).last()
        return {"subscription": subscription}

    return {}

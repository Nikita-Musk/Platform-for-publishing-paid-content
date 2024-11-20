from django.db import models

from users.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    preview = models.ImageField(
        upload_to="post/preview", verbose_name="Превью поста", blank=True, null=True
    )
    is_free = models.BooleanField(verbose_name="Доступно бесплатно", default=False)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Subscription(models.Model):
    SUB_CHOICES = [
        ("one_month", "1 месяц"),
        ("three_month", "3 месяца"),
        ("six_month", "6 месяцев"),
        ("one_year", "1 год"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    type_of_sub = models.CharField(choices=SUB_CHOICES, verbose_name="Тип подписки")
    start_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата старта подписки", blank=True, null=True
    )
    end_date = models.DateTimeField(
        verbose_name="Дата окончания подписки", blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)

    session_id = models.CharField(
        max_length=150, verbose_name="Номер сессии", blank=True, null=True
    )
    link = models.URLField(
        max_length=450, verbose_name="Ссылка на оплату", blank=True, null=True
    )

    def get_price(self):
        price = {
            "one_month": 1500,
            "three_month": 4000,
            "six_month": 6000,
            "one_year": 10000,
        }
        return price.get(self.type_of_sub, 0)

    def __str__(self):
        return f"{self.user} - {self.type_of_sub}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

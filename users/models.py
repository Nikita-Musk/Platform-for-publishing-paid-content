from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    first_name = models.CharField(
        max_length=50, verbose_name="Имя", blank=True, null=True
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия", blank=True, null=True
    )
    email = models.EmailField(unique=True, verbose_name="Почта")
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="Аватар", blank=True, null=True
    )
    phone = models.CharField(max_length=35, unique=True, verbose_name="Телефон")
    token = models.CharField(max_length=6, verbose_name="Токен", blank=True, null=True)
    is_author = models.BooleanField(default=False, verbose_name="Является автором?")

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

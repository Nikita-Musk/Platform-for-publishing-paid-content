from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """Миксин для проверки авторизации пользователя."""

    def handle_no_permission(self):
        """Обрабатка ситуации, когда пользователь не авторизован."""
        messages.error(
            self.request,
            "Пожалуйста, войдите в систему, чтобы получить доступ к этой странице.",
        )
        return redirect(reverse("users:login"))

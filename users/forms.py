from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import User


class CrispyFormMixin:
    """Миксин для использовать расширенные возможности crispy-forms."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class ProfileForm(CrispyFormMixin, UserChangeForm):
    """Форма для изменения профиля пользователя."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "avatar", "phone")

    def __init__(self, *args, **kwargs):
        """Инициализация для скрытия возмодности изменять пароль."""
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()


class AuthorForm(forms.ModelForm):
    """Форма для информации об авторе."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "avatar")


class RegistrationForm(CrispyFormMixin, UserCreationForm):
    """Форма для регистрации нового пользователя."""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
            "is_author",
            "password1",
            "password2",
        )

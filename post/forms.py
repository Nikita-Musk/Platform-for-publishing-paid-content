from crispy_forms.helper import FormHelper
from django.forms import ModelForm

from post.models import Post


class CrispyFormMixin:
    """Миксин для использовать расширенные возможности crispy-forms."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class PostForm(CrispyFormMixin, ModelForm):
    """Форма для создания нового поста."""

    class Meta:
        model = Post
        exclude = ("author",)


class PostUpdateForm(CrispyFormMixin, ModelForm):
    """Форма для обновления существующего поста."""

    class Meta:
        model = Post
        exclude = ("author",)

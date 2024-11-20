from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Создание суперпользователя."""

    def handle(self, *args, **options):
        user = User.objects.create(phone=80297777777)
        user.set_password("admin")
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

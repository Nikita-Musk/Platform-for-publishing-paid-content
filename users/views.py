from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny

from users.forms import AuthorForm, ProfileForm, RegistrationForm
from users.models import User
from users.permissions import CustomLoginRequiredMixin
from users.serializers import RegisterSerializer
from users.services import generate_unique_token


class RegisterView(CreateView):
    """Контроллер для регистрации нового пользователя."""

    model = User
    form_class = RegistrationForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:sms-confirm")

    def form_valid(self, form):
        """Обработка валидной формы регистрации."""
        user = form.save()
        user.is_active = False
        token = generate_unique_token()
        user.token = token
        user.save()
        # Получаем код в консоль для теста
        print(token)

        # Получаем код с платного API twilio, можно передать телефон на который будет отправляться смс.
        # send_sms_for_your_number(token, user.phone)

        self.request.session["token"] = token
        return super().form_valid(form)


def sms_verification(request):
    """Функция для верификации пользователя по смс."""
    token = request.session.get("token")
    user = get_object_or_404(User, token=token)

    if request.method == "POST":
        code = request.POST.get("code")
        if code == user.token:
            user.is_active = True
            user.token = ""
            user.save()
            return redirect(reverse("users:login"))
    return render(request, "users/sms_confirm.html")


class ProfileView(CustomLoginRequiredMixin, UpdateView):
    """Контроллер для редактирования профиля пользователя."""

    model = User
    form_class = ProfileForm
    template_name = "users/profile_from.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        """Возвращает объект пользователя."""
        return self.request.user


class AuthorListView(ListView):
    """Контроллер для списка авторов."""

    model = User
    form_class = AuthorForm

    def get_queryset(self):
        """Возвращает список авторов, отсортированных по фамилии."""
        return User.objects.filter(is_author=True).order_by("last_name")


class RegisterAPIView(CreateAPIView):
    """API для регистрации нового пользователя."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Обработка создания нового пользователя."""
        user = serializer.save()
        user.set_password(user.password)
        user.save()

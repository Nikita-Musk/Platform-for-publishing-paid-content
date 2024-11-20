from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from post.forms import PostForm, PostUpdateForm
from post.models import Post, Subscription
from post.services import (SubscriptionService, create_stripe_session,
                           get_stripe_price)
from users.permissions import CustomLoginRequiredMixin


class IndexView(ListView):
    """Контроллер для отображения главной страницы с последними постами."""

    model = Post
    template_name = "post/base.html"

    def get_queryset(self):
        """Получает последние 3 поста, отсортированные по убыванию id."""
        return Post.objects.all().order_by("-id")[:3]  # или исп


class PostCreateView(CustomLoginRequiredMixin, CreateView):
    """Контроллер для создания нового поста."""

    model = Post
    form_class = PostForm
    success_url = reverse_lazy("post:post-list")

    def form_valid(self, form):
        """Автоустановка автора поста перед его сохранением."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(CustomLoginRequiredMixin, UpdateView):
    """Контроллер для обновления существующего поста."""

    model = Post
    form_class = PostUpdateForm
    success_url = reverse_lazy("post:post-list")


class PostListView(ListView):
    """Контроллер для отображения списка всех постов."""

    model = Post

    def get_queryset(self):
        """Получает все посты, отсортированные в обратном порядке по is_free и названию."""
        return Post.objects.all().order_by("-is_free", "title")


class PostDetailView(DetailView):
    """Контроллер для отображения деталей конкретного поста."""

    model = Post


class PostDeleteView(CustomLoginRequiredMixin, DeleteView):
    """Контроллер для удаления поста."""

    model = Post
    success_url = reverse_lazy("post:post-list")


class ChooseSubView(CustomLoginRequiredMixin, View):
    """Контроллер для выбора типа подписки."""

    template_name = "post/choose_sub.html"

    def get(self, request):
        """Обрабатывает GET-запрос и отображает страницу выбора подписки. Подписки из модели."""
        context = {"subscription_choices": Subscription.SUB_CHOICES}
        return render(request, self.template_name, context)

    def post(self, request):
        """Обрабатывает POST-запрос для создания подписки."""
        # Получаем тип подписки из формы
        type_of_sub = request.POST.get("type_of_sub")
        if SubscriptionService.has_active_subscription(request.user):
            return HttpResponse(
                "У вас уже есть активная подписка. Вы не можете купить новую.",
                status=400,
            )

        request.session["type_of_sub"] = type_of_sub
        subscription = SubscriptionService.create_or_update_subscription(
            request.user, type_of_sub
        )

        return redirect("post:subscription-payment", subscription_id=subscription.id)


class PaymentView(CustomLoginRequiredMixin, View):
    """Контроллер для обработки платежа по подписке."""

    template_name = "post/payment.html"

    def get(self, request, subscription_id):
        """Обрабатывает GET-запрос для отображения страницы оплаты."""
        subscription = get_object_or_404(
            Subscription, id=subscription_id, user=request.user
        )

        price_in_usd = subscription.get_price()

        interval = SubscriptionService.get_subscription_interval(
            subscription.type_of_sub
        )

        price = get_stripe_price(price_in_usd, int(interval))
        session_id, payment_link = create_stripe_session(price)
        subscription.session_id = session_id
        subscription.link = payment_link
        subscription.is_paid = True
        subscription.save()

        # Возвращаем ответ, рендерим шаблон с данными
        return render(
            request,
            self.template_name,
            {
                "subscription": subscription,
                "payment_link": payment_link,
                "price": price_in_usd,
            },
        )


class SubConfirmSuccessView(CustomLoginRequiredMixin, View):
    """Контроллер для отображения страницы успешного подтверждения подписки."""

    template_name = "post/confirm_success.html"

    def get(self, request, *args, **kwargs):
        """Обрабатывает GET-запрос и отображает страницу успешного подтверждения подписки."""
        return render(request, self.template_name)

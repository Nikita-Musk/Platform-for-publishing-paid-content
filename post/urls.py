from django.urls import path

from post.apps import PostConfig
from post.views import (ChooseSubView, IndexView, PaymentView, PostCreateView,
                        PostDeleteView, PostDetailView, PostListView,
                        PostUpdateView, SubConfirmSuccessView)

app_name = PostConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/update/<int:pk>/", PostUpdateView.as_view(), name="post-update"),
    path("post/delete/<int:pk>/", PostDeleteView.as_view(), name="post-delete"),
    path("subscription/", ChooseSubView.as_view(), name="subscription"),
    path(
        "subscription/payment/<int:subscription_id>/",
        PaymentView.as_view(),
        name="subscription-payment",
    ),
    path("subscription/success/", SubConfirmSuccessView.as_view(), name="sub-success"),
]

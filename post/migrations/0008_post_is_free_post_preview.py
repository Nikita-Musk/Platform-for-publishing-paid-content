# Generated by Django 5.1.3 on 2024-11-16 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0007_subscription_end_date_subscription_is_active_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="is_free",
            field=models.BooleanField(default=False, verbose_name="Доступно бесплатно"),
        ),
        migrations.AddField(
            model_name="post",
            name="preview",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="post/preview",
                verbose_name="Превью поста",
            ),
        ),
    ]
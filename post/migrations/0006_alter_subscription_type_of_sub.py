# Generated by Django 5.1.3 on 2024-11-15 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0005_subscription_link_subscription_session_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="type_of_sub",
            field=models.CharField(
                choices=[
                    ("one_month", "1 месяц"),
                    ("three_month", "3 месяца"),
                    ("six_month", "6 месяцев"),
                    ("one_year", "1 год"),
                ],
                verbose_name="Тип подписки",
            ),
        ),
    ]
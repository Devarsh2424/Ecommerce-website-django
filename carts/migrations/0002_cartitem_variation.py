# Generated by Django 5.2.4 on 2025-07-30 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("carts", "0001_initial"),
        ("store", "0002_variation"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="variation",
            field=models.ManyToManyField(blank=True, to="store.variation"),
        ),
    ]

# Generated by Django 5.2.4 on 2025-07-31 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("carts", "0002_cartitem_variation"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cartitem",
            old_name="variation",
            new_name="variations",
        ),
    ]

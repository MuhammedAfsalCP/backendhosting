# Generated by Django 5.1.4 on 2025-01-17 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0010_alter_products_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="Image",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
    ]

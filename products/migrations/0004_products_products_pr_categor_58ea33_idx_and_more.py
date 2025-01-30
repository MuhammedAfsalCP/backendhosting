# Generated by Django 5.1.4 on 2025-01-15 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_alter_products_category"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="products",
            index=models.Index(
                fields=["Category"], name="products_pr_Categor_58ea33_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="products",
            index=models.Index(fields=["Price"], name="products_pr_Price_5c504e_idx"),
        ),
        migrations.AddIndex(
            model_name="products",
            index=models.Index(fields=["Brand"], name="products_pr_Brand_c02c8e_idx"),
        ),
        migrations.AddIndex(
            model_name="products",
            index=models.Index(
                fields=["is_deleted"], name="products_pr_is_dele_6e899d_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="products",
            index=models.Index(
                fields=["product_added"], name="products_pr_product_f52ae4_idx"
            ),
        ),
    ]

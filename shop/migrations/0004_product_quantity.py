# Generated by Django 5.1.1 on 2024-09-24 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_related_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]

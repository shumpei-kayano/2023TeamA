# Generated by Django 4.2 on 2024-02-07 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sale_type',
            field=models.CharField(blank=True, choices=[('general_sales', '一般商品'), ('melimit_sales', '共同商品')], max_length=20, verbose_name='販売タイプ'),
        ),
    ]

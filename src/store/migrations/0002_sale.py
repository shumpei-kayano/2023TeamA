# Generated by Django 4.2 on 2023-11-27 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_alter_melimituser_taste'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale_start', models.DateTimeField()),
                ('sale_end', models.DateTimeField()),
                ('stock', models.IntegerField()),
                ('expiration_date', models.DateField()),
                ('actual_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('sale_type', models.CharField(blank=True, choices=[('common_sales', '一般商品'), ('melimit_sales', '共同販売商品')], max_length=20, verbose_name='販売タイプ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.melimitstore')),
            ],
        ),
    ]

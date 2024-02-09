# Generated by Django 4.2 on 2024-02-09 01:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import store.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=30, verbose_name='商品名')),
                ('product_price', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000000)], verbose_name='定価')),
                ('weight', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)], verbose_name='重量')),
                ('product_image', models.ImageField(blank=True, upload_to='images', verbose_name='商品画像')),
                ('product_category', models.CharField(choices=[('meat', '肉類'), ('vegetables', '野菜'), ('fruit', '果物'), ('fish', '魚介類'), ('other', 'その他')], max_length=20, verbose_name='カテゴリ')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.melimitstore', verbose_name='店舗名')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_price', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000000)], verbose_name='販売価格')),
                ('sale_start', models.DateField(validators=[store.models.validate_date], verbose_name='販売開始日時')),
                ('sale_end', models.DateField(validators=[store.models.validate_date], verbose_name='販売終了日時')),
                ('stock', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)], verbose_name='在庫数')),
                ('expiration_date', models.DateField(validators=[store.models.validate_date], verbose_name='賞味期限')),
                ('description', models.TextField(max_length=500, verbose_name='商品の説明')),
                ('sale_type', models.CharField(choices=[('general_sales', '一般商品'), ('melimit_sales', '共同商品')], max_length=20, verbose_name='販売タイプ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.melimitstore')),
            ],
        ),
        migrations.CreateModel(
            name='Threshold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_rate', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='割引率')),
                ('threshold', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)], verbose_name='しきい値')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.sale')),
            ],
        ),
        migrations.CreateModel(
            name='ThresholdCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='個数')),
                ('price', models.IntegerField(verbose_name='金額')),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_threshold_clear', models.BooleanField(default=False)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.sale')),
                ('threshold', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.threshold')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.melimituser')),
            ],
        ),
    ]

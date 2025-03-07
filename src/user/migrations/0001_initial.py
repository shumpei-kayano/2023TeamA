# Generated by Django 4.2 on 2024-02-13 04:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('co2', models.IntegerField()),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_shipped', models.BooleanField(default=False)),
                ('orderhistory_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.melimitstore')),
                ('orderhistory_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.melimituser')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.sale')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.sale')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.melimituser')),
            ],
            options={
                'unique_together': {('user', 'sale')},
            },
        ),
    ]

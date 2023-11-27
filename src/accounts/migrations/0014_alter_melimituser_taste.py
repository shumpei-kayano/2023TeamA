# Generated by Django 4.2 on 2023-11-21 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_melimituser_taste'),
    ]

    operations = [
        migrations.AlterField(
            model_name='melimituser',
            name='taste',
            field=models.CharField(choices=[('肉', '肉'), ('野菜', '野菜'), ('果物', '果物'), ('魚', '魚')], max_length=20, verbose_name='好み'),
        ),
    ]

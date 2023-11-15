from django.db import models

class Ingredient(models.Model):
    MEAT = 'ME'
    VEGETABLE = 'VE'
    FISH = 'FI'
    OTHER = 'OT'

    CATEGORY_CHOICES = [
        (MEAT, '肉'),
        (VEGETABLE, '野菜'),
        (FISH, '魚'),
        (OTHER, 'その他'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=MEAT)


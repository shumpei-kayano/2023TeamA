from django.db import models
from accounts.models import MelimitStore

# Create your models here.

class Product(models.Model):
    TASTE_CHOICES = (
        ('meat', 'meat'),
    ('vegetables', 'vegetables'),
    ('fruit', 'fruit'),
    ('fish', 'fish'),
        # ('other', 'その他'),
    )

    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.IntegerField()
    product_image = models.ImageField(upload_to='images')
    product_category = models.CharField("カテゴリ", max_length=20, choices=TASTE_CHOICES, blank=True)
    # 外部キーとしてMelimitStoreのidを持つ
    # ログインしているMelimitStoreのidが自動で入る
    store = models.ForeignKey(MelimitStore, on_delete=models.CASCADE)

    #weightに0.4をかける関数
    def CO2(self):
        return str(self.weight * 0.4) + 'kg'
    
    def __str__(self):
        return self.product_name
from django.db import models
from accounts.models import MelimitStore
from django.utils import timezone

# Create your models here.

class Product(models.Model):
    TASTE_CHOICES = (
        ('meat', 'meat'),
        ('vegetables', 'vegetables'),
        ('fruit', 'fruit'),
        ('fish', 'fish'),
        # ('other', 'その他'),
    )

    product_name = models.CharField(max_length=200, verbose_name='商品名')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='定価')
    weight = models.IntegerField(verbose_name='重量')
    product_image = models.ImageField(upload_to='images', verbose_name='商品画像')
    product_category = models.CharField("カテゴリ", max_length=20, choices=TASTE_CHOICES, blank=True)
    # 外部キーとしてMelimitStoreのidを持つ
    # ログインしているMelimitStoreのidが自動で入る
    store = models.ForeignKey(MelimitStore, on_delete=models.CASCADE, verbose_name='店舗名')

    #weightに0.4をかける関数
    def CO2(self):
        return str(self.weight * 0.4) + 'kg'

    def __str__(self):
        return self.product_name

class Sale(models.Model):
    SALE_CHOICES = (
        ('general_sales', '一般商品'),
        ('melimit_sales', '共同販売商品'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(MelimitStore, on_delete=models.CASCADE)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='販売価格')
    sale_start = models.DateTimeField(verbose_name='販売開始日時')
    sale_end = models.DateTimeField(verbose_name='販売終了日時')
    # 在庫数
    stock = models.IntegerField(verbose_name='在庫数')
    # 賞味期限
    expiration_date = models.DateField(verbose_name='賞味期限')
    # 商品の説明
    description = models.TextField(verbose_name='商品の説明')
    # 一般商品か、共同販売商品か選択するchoiceフィールド、選択肢は共同販売商品、一般商品
    sale_type = models.CharField("販売タイプ", max_length=20, choices=SALE_CHOICES, blank=True)

    def __str__(self):
        return self.product.product_name
    
    # 現在時刻から終了までの期間を計算する関数
    def remaining_time(self):
        return self.sale_end - timezone.now()
    
    # 値引き率を計算する関数
    def discount_rate(self):
        return round((1 - self.sale_price / self.product.product_price) * 100)
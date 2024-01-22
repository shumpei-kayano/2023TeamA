from django.db import models
from accounts.models import MelimitStore
from django.utils import timezone

# Create your models here.

# Djangoのchoicesフィールドでは、選択肢をタプルのリストとして定義します。
# 各タプルの最初の要素はデータベースに保存される実際の値で、
# 2番目の要素はその値を人間が読める形式で表示するためのものです。
# したがって、テンプレートでsale_typeを表示するときには、
# get_<field_name>_displayメソッドを使用して、人間が読める形式の値を取得します。
# このメソッドはDjangoが自動的に各choicesフィールドに対して生成します。

class Product(models.Model):
    TASTE_CHOICES = (
        ('meat', '肉類'),
        ('vegetables', '野菜'),
        ('fruit', '果物'),
        ('fish', '魚介類'),
        ('other', 'その他'),
    )

    product_name = models.CharField(max_length=100, verbose_name='商品名')
    product_price = models.IntegerField(verbose_name='定価')
    # product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='定価')
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
    sale_price = models.IntegerField(verbose_name='販売価格')
    # sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='販売価格')
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
    
    # 注文履歴modelに設定する
    # 発送状況(登録時は未発送)
    # DjangoのBooleanFieldは、データベースレベルではTINYINT型として表現されます。その値は0（False）または1（True）になります。
    # is_shipped = models.BooleanField("発送状況", default=False)

    def __str__(self):
        return self.product.product_name
    
    # 現在時刻から終了までの期間を計算する関数
    def remaining_time(self):
        return self.sale_end - timezone.now()
    
    # 値引き率を計算する関数
    def discount_rate(self):
        return round((1 - self.sale_price / self.product.product_price) * 100)

# しきい値model
class Threshold(models.Model):
    # 割引率(%表示)
    discount_rate = models.IntegerField(verbose_name='割引率')
    # しきい値(個数)
    threshold = models.IntegerField(verbose_name='しきい値')
    # saleの外部キー
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)

    def __str__(self):
        # product_nameとMelimitStoreモデルのusernameを取得し、usernameのproduct_nameのしきい値という形で表示する
        return self.sale.store.username + '：' + self.sale.product.product_name + 'のしきい値'
    
    # 割引率とsale_priceから割引額を計算する関数
    def discount_amount(self):
        return round(self.sale.sale_price * self.discount_rate / 100)
from django.db import models
from django.utils import timezone
from store.models import *
from accounts.models import *
from decimal import Decimal
from django.conf import settings
# Create your models here.

# 注文履歴クラス
class OrderHistory(models.Model):
    # 外部キーとしてProductのidを持つ
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # 外部キーとしてSaleのidを持つ
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    # 外部キーとしてMelimitStoreのidを持つ
    orderhistory_store = models.ForeignKey(MelimitStore, on_delete=models.CASCADE)
    # 外部キーとしてMelimitUserのidを持つ
    orderhistory_user = models.ForeignKey(MelimitUser, on_delete=models.CASCADE)
    # 金額
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField()
    # 数量
    quantity = models.IntegerField()
    # CO2排出量
    # co2 = models.DecimalField(max_digits=10, decimal_places=2)
    co2 = models.IntegerField()
    # 注文日時
    order_date = models.DateTimeField(default=timezone.now)
    # 配送方法
    # delivery_option = models.CharField(max_length=200)
    # 発送済みフラグ(trueが発送済み)
    is_shipped = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.sale.stock -= self.quantity
        self.sale.save()
        # 注文の数量を考慮したco2の計算
        self.co2 = round(self.product.weight * 0.4 * self.quantity)  # 結果を整数にするため四捨五入
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     self.sale.stock -= self.quantity
    #     self.sale.save()
    #     self.co2 = Decimal(self.product.weight * 0.4 * self.quantity)  # 注文の数量を考慮したco2の計算
    #     super().save(*args, **kwargs)

# このコードでは、save()メソッドが一度だけ呼び出されています。
# ただし、2つの異なるオブジェクトに対してsave()が呼び出されています。
# self.sale.save(): ここでは、OrderHistoryオブジェクトが関連付けられているSaleオブジェクトのsave()メソッドが呼び出されています。
# これは、self.sale.stock -= self.quantityで在庫数を減らした後、その変更をデータベースに保存するために必要です。
# super().save(*args, **kwargs): ここでは、OrderHistoryオブジェクト自体のsave()メソッドが呼び出されています。
# これは、OrderHistoryオブジェクトのco2フィールドを計算した後、その変更をデータベースに保存するために必要です。super().save(*args, **kwargs)は、
# 親クラス（models.Model）のsave()メソッドを呼び出しています。これにより、OrderHistoryオブジェクトの全てのフィールドがデータベースに保存されます。

# お気に入りモデル
class Favorite(models.Model):
    user = models.ForeignKey(MelimitUser, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'sale')

    def __str__(self):
        return f'{self.user.username} likes {self.sale.product.product_name}'
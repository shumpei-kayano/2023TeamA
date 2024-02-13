
from store.models import Product,Sale,Threshold,ThresholdCheck
from user.models import OrderHistory
#viewで使う処理
def get_all_products():
    products = Product.objects.all()
    return products
#商品が共同商品のとき、product,sale,threshold,thresholdcheck当たりの情報を取得する処理
#一般も共同も両方ここで処理　indexで使用　
# saleオブジェクト取得してる際に使える関数
def melmit_product_detail(sale):
    #ほしいもの　インデント一括調節　範囲指定後シフトtab
    #pk product or sale pk
    #画像 product.product_image,
    #値引き率 sale.discount_rate(),
    #商品名 :product.product_name,
    #販売価格 sale.sale_price,
    #閾値クリア後の割引率 threshold.discount_rate,
    #クリア後の値段 threshold.discount_amount(),
    #閾値個数 threshold.threshold,
    #現在の閾値個数 チェックモデルから count  check.sum_count() checkはthreshold.thresholdcheck_set.all()が空じゃないときにfor文でループの時 for checkのcheck
    #閾値をクリアしているか確認→クリア後が表記変わるため　countとthresholdを比較するだけ
    #returnの変数の中身に辞書を入れる
    if sale.sale_type == 'general_sales':
        detail = {
            'pk':sale.pk,
            'image': sale.product.product_image,
            'rate': sale.discount_rate(),
            'product_name': sale.product.product_name,
            'price': sale.sale_price,
            'sale_type': sale.sale_type,
            'product_category': sale.product.product_category,
        }
        return detail
    else:
        count = 0
        for threshold in sale.threshold_set.all():
            threshold_checks = threshold.thresholdcheck_set.all()
            if not threshold_checks:
                #空の時、個数を０で判断するように
                count = 0
                print("No threshold checks found, meow!")
            else:
                for check in threshold_checks:
                    #中身があるとき、個数を取り出して合計して判断 sale.pkで閾値チェックモデル化からsumで数量を取得
                    count = check.sum_count()
                    print('check:',check)
                    print('count:',count)
            at_count = threshold.threshold - count
            discounted_price = round(sale.sale_price * (100 - threshold.discount_rate) / 100)
            productprice_thresholdprice = sale.discount_rate() + threshold.discount_rate
            ratio = round(count / threshold.threshold * 100)
            detail = {
                'pk':sale.pk,
                'image': sale.product.product_image,
                'rate': sale.discount_rate(),
                'product_name': sale.product.product_name,
                'price': sale.sale_price,
                'threshold_rate': threshold.discount_rate,
                'clear_price': discounted_price,
                'threshold': threshold.threshold,
                'threshold_now': count,
                'sale_type': sale.sale_type,
                'at_count': at_count,
                'product_category': sale.product.product_category,
                'final_rate':productprice_thresholdprice,
                'ratio':ratio,
                'treshold_rate':threshold.discount_rate,
                'stock':sale.stock,
                'store':sale.store,
                'sale_end':sale.sale_end,
                'description':sale.description,
                'store_name':sale.product.store.username,
                'email':sale.product.store.email,
                'store_url':sale.store.site_url,
                'product_price':sale.product.product_price,
            }
        return detail
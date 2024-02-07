from apscheduler.schedulers.background import BackgroundScheduler
from store.models import ThresholdCheck
from user.models import OrderHistory
from django.utils import timezone

def threshold_timecheck():# 任意の関数名
    # ここに定期実行したい処理を記述する
    print ("定期実行")
    # 設定した時刻を定義します。
    # time_check = datetime.now() # datetimeはtimezoneを考慮しないので、timezone.now()を使う
    time_check = timezone.now() # timezone.now()はUTCを返す
    # time_check = timezone.localtime(timezone.now()) # timezone.localtime()でsettingで設定したTIME_ZONEに変換される
    print(timezone.get_current_timezone_name()) # settingで設定したTIME_ZONEを確認
    print(time_check)
    # recordsにThresholdCheckモデルのsale.sale_endがtime_checkより大きいものを取得
    t_checks = ThresholdCheck.objects.filter(sale__sale_end__lt=time_check, is_threshold_clear=False)
    # recordsが存在する場合の処理
    if t_checks.exists():
        print("存在する")
        print(t_checks)
    else:
        print("存在しない")
        print(t_checks)
    # recordsをループして、要素を出力
    for t in t_checks:
        # recordのsale_idをからsaleを取得
        sale = t.sale
        print(sale)
        orderhistory_copy = OrderHistory(sale=t.sale, product=t.sale.product, orderhistory_store=t.sale.store, orderhistory_user=t.user, amount=t.sale.sale_price, quantity=t.count,)
        # print(orderhistory_copy.__class__())
        orderhistory_copy.save()

def start():
    scheduler = BackgroundScheduler()
    # 1分ごとに実行する
    # scheduler.add_job(threshold_timecheck, 'cron', minute="*")
    # 15秒ごとに実行する
    # scheduler.add_job(threshold_timecheck, 'interval', seconds=15)
    # 1日ごとに実行する
    # scheduler.add_job(threshold_timecheck, 'cron', hour=0, minute=0)
    scheduler.start()
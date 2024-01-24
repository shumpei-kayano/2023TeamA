from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler

def periodic_execution():# 任意の関数名
    # ここに定期実行したい処理を記述する
    print ("定期実行")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_execution, 'cron', minute="*")
    scheduler.start()
import datetime

import schedule

def job():
    now = datetime.datetime.now()
    print(now)

# 每秒执行一次
schedule.every(1).seconds.do(job)

while True:
    # 启动服务
    schedule.run_pending()

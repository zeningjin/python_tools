#
# BROKER_URL = 'redis://localhost' # 使用Redis作为消息代理
#
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0' # 把任务结果存在了Redis
#
# CELERY_TASK_SERIALIZER = 'msgpack' # 任务序列化和反序列化使用msgpack方案
#
# CELERY_RESULT_SERIALIZER = 'json' # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
#
# CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间
#
# CELERY_ACCEPT_CONTENT = ['json', 'msgpack'] # 指定接受的内容类型
from datetime import timedelta


# BROKER_URL = "redis://:@127.0.0.1:6379/1"
BROKER_URL = "amqp://admin:admin@localhost:5672//"
# CELERY_RESULT_BACKEND = "amqp" 已经弃用 celery==4.4.6可用
CELERY_RESULT_BACKEND = "redis://:@127.0.0.1:6379/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_EXPIRES = 60 * 60
# CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERY_TASK_TIME_LIMIT = 60 * 60

# 需要执行任务的配置
CELERYBEAT_SCHEDULE = {
    'test2': {
        'task': 'celery_test.tasks.test',
        # 设置定时的时间，10秒一次nc
        'schedule': timedelta(seconds=10),
        'args': ()
    }
}
import time
from celery_test.app_test import app

@app.task
def add(x, y):
    time.sleep(1)
    return x + y

@app.task
def test():
    r1 = add.delay(1, 2)
    r2 = add.delay(2, 4)
    r3 = add.delay(3, 6)
    r4 = add.delay(4, 8)
    r5 = add.delay(5, 10)
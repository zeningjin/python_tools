import random
import time
from concurrent.futures.thread import ThreadPoolExecutor
from queue import Queue

Send_pool = ThreadPoolExecutor(5)
Send_data_q = Queue()

def send(region):
    x = Send_data_q.get()
    print("获取成功", x)

def set():
    a = random.randint(0, 2)
    Send_data_q.put(a)
    print("插入成功", a)
    time.sleep(1)

region = 1


if __name__ == '__main__':
    """
        数据存入队列后，再取出来
    """
    while True:
        # 启动服务
        Send_pool.submit(send, region)
        time.sleep(1)
        set()
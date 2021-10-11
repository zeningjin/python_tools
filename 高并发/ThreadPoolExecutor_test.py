import time
from concurrent import futures


def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        pass
    # time.sleep(2)
    return fib(n-1) + fib(n-2)
# 使用线程池实现异步处理

# base
with futures.ThreadPoolExecutor() as executor:
    f1 = executor.submit(fib, 4) # return future
    f2 = executor.submit(fib, 5)

print(f1.result())
print(f2.result())
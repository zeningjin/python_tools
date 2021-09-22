import time


def display_time(fun):
    def wrapper(*args):
        print(*args)
        t1 = time.time()
        fun(*args)
        t2 = time.time()
        print(t2 - t1)
    return wrapper



def is_prime(num):
    if num < 2:
        return False
    elif num == 2:
        return True
    else:
        for i in range(2, num):
            if num % i == 0:
                return False
        else:
            return True


@display_time
def count_prime_nums(maxnum):
    count = 0
    for i in range(2, maxnum):
        if is_prime(i):
            count += 1
    print(count)

if __name__ == '__main__':
    count_prime_nums(20000)
import threading
import time

def music(name, n, a):
    for i in range(n):
        time.sleep(1)
        print('听音乐%s第%s次' % (name, i))
    a.append('111')


def movie(name, n, b):
    for i in range(n):
        time.sleep(2)
        print('看电影%s第%s次' % (name, i))
    b.append('222')


if __name__ == '__main__':
    thread_list = []
    a = []
    b = []
    t1 = threading.Thread(target=music, args=('野狼Disco', 10, a))  # 泛函编程，函数式编程
    t2 = threading.Thread(target=movie, args=('哪吒', 10, b))
    t1.start()
    t2.start()
    # print(a[0], 1111)
    # print(b[0], 22222)

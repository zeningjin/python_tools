# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 下午8:36
# @Author  : jinzening
# @File    : django.py
# @Software: PyCharm

import unittest


# 方式一：unittest.main()来启动单元测试模块
class MyTestCase(unittest.TestCase):
    def setUp(self):
        print('测试环境')

    def test(self):
        print('测试用例')
        self.assertEquals(4, 2 * 2)
        self.assertEqual(1, 3, 'something was wrong')

    def tearDown(self):
        print('环境销毁')


if __name__ == '__main__':
    unittest.main()

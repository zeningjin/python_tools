# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 下午8:06
# @Author  : jinzening
# @File    : 基础.py
# @Software: PyCharm
import unittest
from time import sleep

from selenium import webdriver


class Test_Demo(unittest.TestCase):
    # 前置条件
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://www.baidu.com")

    # 后置条件
    def tearDown(self):
        sleep(3)
        self.driver.quit()

    # 测试，按照名称字符串大小进行先后运行
    @unittest.skip
    def test_2_one(self):
        print("欢迎您")

    @unittest.skip
    def test_1_two(self):
        print("欢迎您,啦啦啦")

    def test_3_three(self):
        # self.driver = webdriver.Chrome()
        # self.driver.get("http://www.baidu.com")
        self.driver.find_element_by_id('kw').send_keys('靳泽宁')
        self.driver.find_element_by_id('su').click()

if __name__ == '__main__':
    unittest.main()

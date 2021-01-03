# -*- coding: utf-8 -*-
# @Time    : 2020/10/12 下午8:41
# @Author  : jinzening
# @File    : 腾讯云.py
# @Software: PyCharm
# import requests
# # 腾讯云banana
# url = 'https://cloud.tencent.com/'
# res = requests.get(url=url)
# print(res.text)


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 自动打开游览器
browser = webdriver.Chrome()
browser.get('https://cloud.tencent.com/')


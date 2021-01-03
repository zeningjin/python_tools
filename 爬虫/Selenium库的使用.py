# -*- coding: utf-8 -*-
# @Time    : 2020/10/21 上午9:17
# @Author  : jinzening
# @File    : Selenium库的使用.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# # 自动打开游览器
# browser = webdriver.Chrome()
# browser.get('https://www.csdn.net/')

driver = webdriver.Chrome()
driver.get("https://help.aliyun.com/noticelist/9965003.html?spm=a2c4g.11174386.n2.2.34a87cbbzooKbp")
#断言
assert "Python" in driver.title
# # 通过name属性找到搜索框
# elem = driver.find_element_by_name("q")
# # 在搜索框内输入内容
# elem.send_keys("pycon")
# # 提交
# elem.send_keys(Keys.RETURN)
# 打印网页源代码
print(driver.page_source)


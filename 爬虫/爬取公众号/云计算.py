# -*- coding: utf-8 -*-
# 所有公众号获取文章为距当前日期最近的一天所有文章
# 正文前五行未爬取成功  以及爬取公众号文章不一定是字体，可能有图片。
from selenium import webdriver
import time
import json
import requests
import re
import random
from lxml import etree
from chardet import detect

#爬取的公众号列表
gzlist = ['华为云', '阿里云', 'Ucloud云计算', 'AWS云计算', 'Zenlayer', '云头条', 'IDC', 'Gartner', 'CSDN云计算', '腾讯云']


def weChat_login():
    #定义一个空的字典，存放cookies内容
    post = {}
    print("启动浏览器，打开微信公众号登录界面")
    driver = webdriver.Chrome(executable_path='C:\chromedriver.exe')
    driver.get('https://mp.weixin.qq.com/')
    time.sleep(5)
    print("正在输入微信公众号登录账号和密码......")
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[2]/a").click()
    driver.find_element_by_xpath("//*[@id='header']/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input").clear()
    # 自动填入登录用户名
    driver.find_element_by_xpath("//*[@id='header']/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input").send_keys("jpyljl@163.com")
    # 清空密码框中的内容
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input").clear()
    # 自动填入登录密码
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input").send_keys("1998.11.23")
    print("请在登录界面点击:记住账号")
    time.sleep(10)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/div[1]/form/div[4]/a").click()
    # 拿手机扫二维码！
    print("请拿手机扫码二维码登录公众号")
    time.sleep(20)
    print("登录成功")
    driver.get('https://mp.weixin.qq.com/')
    cookie_items = driver.get_cookies()
    for cookie_item in cookie_items:
        post[cookie_item['name']] = cookie_item['value']
    cookie_str = json.dumps(post)
    with open('cookie.txt', 'w+', encoding='utf-8') as f:
        f.write(cookie_str)
    print("cookies信息已保存到本地")


def get_content(query):
    url = 'https://mp.weixin.qq.com'
    header = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        }
    with open('cookie.txt', 'r', encoding='utf-8') as f:
        cookie = f.read()
    cookies = json.loads(cookie)
    response = requests.get(url=url, cookies=cookies)
    token = re.findall(r'token=(\d+)', str(response.url))[0]
    #搜索微信公众号的接口地址
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    #搜索微信公众号接口需要传入的参数，有三个变量：微信公众号token、随机数random、搜索的微信公众号名字
    query_id = {
        'action': 'search_biz',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'query': query,
        'begin': '0',
        'count': '1'
        }
    #打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers
    search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
    lists = search_response.json().get('list')[0]    # 搜索结果中的第一个公众号
    fakeid = lists.get('fakeid')   # 获取这个公众号的fakeid，后面爬取公众号文章需要此字段
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'  #  微信公众号文章接口地址
    query_id_data = {
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',      #不同页，此参数变化，变化规则为每页加1  取出最近更新的文章
        'count': '1',
        'query': '',
        'fakeid': fakeid,
        'type': '9'
        }
    query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    fakeid_list = query_fakeid_response.json().get('app_msg_list')
    print(fakeid_list)
    for item in fakeid_list:
        content_link = item.get('link')
        content_title = item.get('title')
        url = content_link
        res = requests.get(url)
        ecoding = detect(res.content).get('encoding')
        data = res.content.decode(ecoding)
        ele = etree.HTML(data)
        contents = ele.xpath("//*[@id='js_content']//text()")  # 获取全部内容
        content = contents[1]
        fileName = query + '.txt'
        with open(fileName, 'a', encoding='utf-8') as fh:
            fh.write(content_title + ":\n" + content_link + "\n" + content + "\n")


if __name__ == '__main__':
    try:
        #登录微信公众号，获取登录之后的cookies信息，并保存到本地文本中
        weChat_login()
        #登录之后，通过微信公众号后台提供的微信公众号文章接口爬取文章
        for query in gzlist:
            #爬取微信公众号文章，并存在本地文本中
            print("开始爬取公众号："+query)
            get_content(query)
            print("爬取完成")
    except Exception as e:
        print(str(e))

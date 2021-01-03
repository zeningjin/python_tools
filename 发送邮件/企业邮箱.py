# -*- coding: utf-8 -*-
# @Time    : 2020/10/11 下午7:01
# @Author  : jinzening
# @File    : 企业邮箱.py
# @Software: PyCharm

import smtplib  # smtp服务器
from email.mime.text import MIMEText  # 邮件文本

# 邮件构建

url = r'http://10.13.225.228:8082/api/mail/'
receiver = "dengke.tang@capitalonline.net"
subject = "测试邮件接口连通"
content = "resop OK!"

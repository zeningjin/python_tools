# -*- coding: utf-8 -*-
# @Time    : 2020/10/26 下午8:54
# @Author  : jinzening
# @File    : 爬取照片.py
# @Software: PyCharm
import requests
from urllib import request
import json
pagenum = 0
num = 0
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "BAIDUID=30249F8D341738F1806EF0EDCED8B235:FG=1; BIDUPSID=30249F8D341738F1806EF0EDCED8B235; PSTM=1593140831; BDUSS=F6M2RRRDV-eWFHTFJtU1hvcjU2OEkzbW1kUms2d1I5YmNoT3JrVkVxUjBPQjFmSVFBQUFBJCQAAAAAAAAAAAEAAACPlt2kysC958jntMu082dvAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHSr9V50q~VeNn; indexPageSugList=%5B%22%E5%A3%81%E7%BA%B8%22%2C%22%E9%BB%91%E8%89%B2%E5%A3%81%E7%BA%B8%22%2C%22%E9%BB%91%E8%89%B2%E5%8A%B1%E5%BF%97%E5%A3%81%E7%BA%B8%22%2C%22%E4%BD%A0%E8%BF%98%E6%9C%89%E5%A5%BD%E5%A4%9A%E6%9C%AA%E5%AE%8C%E6%88%90%E7%9A%84%E6%A2%A6%20%E9%AB%98%E6%B8%85%22%2C%22%E4%BD%A0%E8%BF%98%E6%9C%89%E5%A5%BD%E5%A4%9A%E6%9C%AA%E5%AE%8C%E6%88%90%E7%9A%84%E6%A2%A6%22%5D; BDUSS_BFESS=F6M2RRRDV-eWFHTFJtU1hvcjU2OEkzbW1kUms2d1I5YmNoT3JrVkVxUjBPQjFmSVFBQUFBJCQAAAAAAAAAAAEAAACPlt2kysC958jntMu082dvAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHSr9V50q~VeNn; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; yjs_js_security_passport=5aa3644a5c4df99b54229f4cd78e3f4f94e80c04_1603676202_js; delPer=0; BDRCVFR[8gzLr2xelNt]=IdAnGome-nsnWnYPi4WUvY; BAIDUID_BFESS=54BC0F758875EBB270AAABFF5190F7D5FG=1; PSINO=5; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; firstShowTip=1; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; H_PS_PSSID=32811_1468_32876_31253_32723_32230_7516_7605_32115_31709_32918",
    "Host": "image.baidu.com",
    "Referer": "https//image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&fm=index&pos=history&word=%E5%A3%81%E7%BA%B8",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
while True:
    url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%96%97%E5%9B%BE&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word=%E6%96%97%E5%9B%BE&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn="+str(pagenum)+"&rn=30"
    pagenum += 30
    res = json.loads(requests.get(url, headers=headers).text)
    for i in res['data']:
        # 获取图片的url
        # 常用ele.xpath("//*[@id='imglist']/div[1]/a[1]/img/@img")
        print(i['thumbURL'])
        # 保存图片
        request.urlretrieve(i["hoverURL"], r"/home/zening/文档/工作文档/数据库插数据/爬虫/request爬取/save_image/"+str(num)+".jpg")
        num += 1

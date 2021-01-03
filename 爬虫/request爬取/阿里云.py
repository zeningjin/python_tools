# -*- coding: utf-8 -*-
import json

import requests
# 阿里云banana
import datetime
aly_bananas = {}
headers = {
    "content-type": "application/x-www-form-urlencoded",
    "cookie": "cna=KE9uF1EN/UICAXJwVMZBB5Ou; UM_distinctid=1731dc0d9e84-0aceb07260c23e-39770e5a-1fa400-1731dc0d9e9159; aliyun_choice=CN; _ga=GA1.2.1798008334.1602508079; aliyun_lang=zh; t=9a4b38ba932a86706fb65eaa3e9ec1dc; _tb_token_=3e7a55731e53e; cookie2=1079f2534a4be9ba055ef75785897ff1; ping_test=true; _samesite_flag_=true; _hvn_login=6; csg=528c8124; login_aliyunid_ticket=n_NVkfBTq8cgk4BjngR3wvcao4u4wISJkyRbUddf_YNpoU_BOTwChTBoNM1ZJeedfK9zxYnbN5hossqIZCr6t7SGxRigm2Cb4fGaCdBZWIzmgdHq6sXXZQg4KFWufyvpeV*0*Cm58slMT1tJw3_G$$P00; login_aliyunid_luid=BG+6onWC9cE6e81b36cbc5023afc991b84e9003ebda+EVbGSXagS3odiXyCj9zQXi7AkjR4wumAI3zBMdix; login_aliyunid_csrf=_csrf_tk_1590203415215905; login_aliyunid_pk=1206002509150211; hssid=1zmgu5hEWDuUXd-jsTHV0qQ1; hsite=6; aliyun_country=CN; aliyun_site=CN; login_aliyunid_pks=BG+HQLhrIQoAIEelihBqAoouLuvfLJnlJrXY0mqx+aSD/o=; login_aliyunid_abi=BG+dysG407I0b3f431d60b19591f926d403fe6401e6+5NvMF6S+By3SgLxY/KutCTW5tavHDbeh5BVzZ75LT48Zxdu0GOo=; login_aliyunid=%E6%A2%A6%E7%9A%84%E9%A3%9E%E7%BF%9411qw; xlly_s=1; JSESSIONID=9A1220DC707A69CBA5DF321BA19C36C0; l=eBPTkLrROQcM3kdUKOfwourza77OSIRAguPzaNbMiOCPO51v5PUGWZWVcXLJC3GVh6yWR3RZ-DG7BeYBYIvSbXfNAW8a9WHmn; tfstk=cya1BEs3FbDUmaS2751E_AbNA33FZTYIteDU1lIc78vFkAP1irYrFtCS1pTK2X1..; isg=BKqqD9A_gfdjjg0IHd8SThJC-xlMGy51l2qo6zRjVv2JZ0ohHKt-hfCR95P7l6YN",
    "origin": "https://www.aliyun.com",
    "referer": "https://www.aliyun.com/?accounttraceid=82ea76339a1545f1a5a07256bf7246b7vswo",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}
url = 'https://bridge.aliyun.com/abs/home/queryBannerPlan'
data = {
    'adPlanQueryParam': '{"adZone":{"positionList":[{"positionId":"402"},{"positionId":"403"},{"positionId":"405"},{"positionId":"406"},{"positionId":"407"}]},"requestId":"5e15f486-5460-480a-a6f8-bea0ffe153d0"}'
}
banner_title_list = []
banner_url_list = []
name_list = []
res = json.loads(requests.post(url=url, headers=headers, data=data).text)
banner_message_dicts = res.get('data').get("positionAdPlanMap")
for banner_id, banner_message_data in banner_message_dicts.items():
    banner_message = json.loads(banner_message_data[0].get("displayContent"))
    banner_name_info = banner_message.get("infoList")[0]
    banner_title = banner_name_info.get("title")
    banner_url = banner_name_info.get("link")
    name = banner_name_info.get("description")
    if banner_title and banner_url and name:
        banner_title_list.append(banner_title)
        banner_url_list.append(banner_url)
        name_list.append(name)
print(banner_title_list)
print(banner_url_list)
print(name_list)







# -*- coding: utf-8 -*-
# @Time    : 2020/10/28 上午11:28
# @Author  : jinzening
# @File    : re_chandao_product.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2020/10/19 下午4:02
# @Author  : jinzening
# @File    : chandao_product.py
# @Software: PyCharm
import requests
import json
import datetime
from lxml import etree
from hashlib import md5
import logging
from chinese_calendar import is_workday


class Zentao(object):

    def __init__(self, host, account, password):
        self.host = host
        self.session_id = ''
        self.params = {}
        self.account = account
        self.password = password
        self._get_session_id()
        self.login()

    def _get_session_id(self):
        api_path = "/zentao/api-getsessionid.json"
        response = requests.get(self.host + api_path)
        result = self._get_zentao_result(response.json())
        self.session_id = result['sessionID']
        self.params[result['sessionName']] = self.session_id

    def login(self):
        api_path = '/zentao/user-login.json'
        data = {
            'account': self.account,
            'password': self.password,
        }
        result = requests.post(self.host + api_path, data=data, params=self.params).json()
        if result['status'] == 'success':
            print(self.account + '登陆成功')
        else:
            print(result)

    @staticmethod
    def _get_zentao_result(result):
        if result['status'] == 'success' and md5(result['data'].encode()).hexdigest() == result['md5']:
            data = json.loads(result['data'])
            return data
        return result


    def get_project_demand_remark_by_project_demand_id(self, project_demand_id):
        """
        通过project_demand_id获取该任务的备注
        :param task_id:
        :return:
        """
        remark_data = {}
        path = '/zentao/story-view-' + str(project_demand_id) + '.html'
        print('开始获取' + str(project_demand_id) + '历史记录 url为：')
        res = self.zentao_get(path)
        ele = etree.HTML(res)
        project_demand_remaek = ele.xpath("//*[@id='actionbox']/div[2]/ol/li/text()[1]")
        all_number = len(project_demand_remaek)
        print(all_number, 'all_number')
        if all_number <= 1:
            return remark_data
        for i in range(2, all_number + 1):
            try:
                update_time = ele.xpath("//*[@id='actionbox']/div[2]/ol/li[" + str(i) + "]/text()[1]")[0].split(',')[0].strip()
                update_people = ele.xpath("//*[@id='actionbox']/div[2]/ol/li[" + str(i) + "]/strong/text()")[0].strip()
                update_type = ele.xpath("//*[@id='changeBox" + str(i + 1) + "']/strong/i/text()")[0].strip()
            except:
                continue
            if update_type == '所处阶段':
                update_context = ele.xpath("//*[@id='changeBox" + str(i + 1) + "']/text()[2]")
                update_context_end = update_context[0].split('"')[-2]
                remark_data[i] = {
                    'update_time': update_time,
                    'update_people': update_people,
                    'update_context_end': update_context_end,
                }
        print(remark_data, project_demand_id, '备注信息')
        return remark_data


    def get_project_ids(self):
        """
        获取所有的项目id
        :return:
        """
        path = '/zentao/product-all-38--all.html'
        print('开始获取项目的所有数量 url为')
        res = self.zentao_get(path)
        ele = etree.HTML(res)
        project_ids = []
        all_number = ele.xpath("//*[@id='all']/span[2]/text()")
        if all_number:
            new_path = '/zentao/product-all-32--all-order_desc-' +\
                       str(all_number[0].strip()) + '-' + str(all_number[0].strip()) + '-1.html'
            print('开始获取所有的项目id号 url为：')
            res = self.zentao_get(new_path)
            ele = etree.HTML(res)
            project_ids = ele.xpath("////*[@id='productTableList']/tr/td[1]/text()")
        return [project_id.strip() for project_id in project_ids]

    def get_project_demand_by_project_ids(self, project_ids = []):
        project_demand_data = {}
        for project_id in project_ids:
            path = '/zentao/product-browse-' + str(project_id) + '-0-allstory.html'
            print('开始获取' + project_id + '项目需求的数量 url为：')
            res = self.zentao_get(path)
            ele = etree.HTML(res)
            all_number = ele.xpath("//*[@id='allstoryTab']/span[2]/text()")
            print(all_number, '数量信息')
            if all_number:
                project_demand_data[project_id] = {}
                new_path = '/zentao/product-browse-' + str(project_id) + '-0-allstory-0--' +\
                           str(all_number[0].strip()) + '-' + str(all_number[0].strip()) + '-1.html'
                print('开始获取所有的项目需求的内容 url为：')
                res = self.zentao_get(new_path)
                ele = etree.HTML(res)
                # 开始便利表格，获取所有的产品需求数据
                for i in range(int(all_number[0].strip())):
                    project_name = ele.xpath("//*[@id='currentItem']/text()")
                    project_demand_id = ele.xpath("//*[@id='storyList']/tbody/tr[" + str(i) + "]/td[1]/a/text()")
                    project_demand_name = ele.xpath("//*[@id='storyList']/tbody/tr[" + str(i) + "]/td[3]/a/text()")
                    project_demand_create_people = ele.xpath("//*[@id='storyList']/tbody/tr[" + str(i) + "]/td[5]/text()")
                    project_demand_appoint_people = ele.xpath("//*[@id='storyList']/tbody/tr[" + str(i) + "]/td[6]/a/span/text()")
                    project_demand_stage = ele.xpath("//*[@id='storyList']/tbody/tr[" + str(i) + "]/td[9]/text()")
                    if not project_demand_stage:
                        project_demand_stage = ele.xpath("//*[@id='storyList']/tbody/tr[" + str(i) + "]/td[9]/div/text()")
                    print(project_name, project_demand_id, project_demand_name,
                          project_demand_create_people, project_demand_appoint_people, project_demand_stage)
                    if project_demand_appoint_people == ['Closed'] or project_demand_appoint_people == ['未指派']:
                        continue
                    if project_demand_id and project_demand_name and\
                            project_demand_create_people and project_demand_appoint_people and project_demand_stage:
                        project_demand_id = project_demand_id[0].strip()
                        project_demand_data[project_id][project_demand_id] = {
                            'project_name': project_name[0].strip(),
                            'project_demand_id': project_demand_id,
                            'project_demand_name': project_demand_name[0].strip(),
                            'project_demand_create_people': project_demand_create_people[0].strip(),
                            'project_demand_appoint_people': project_demand_appoint_people[0].strip(),
                            'project_demand_stage': project_demand_stage[0].strip()
                        }
        print(project_demand_data, 'project_demand_data')
        return project_demand_data

    def zentao_get(self, api_path):
        print(self.host + api_path)
        response = requests.get(self.host + api_path, self.params)
        # print(response.content)
        return response.text


class ProductData(Zentao):

    def __init__(self, host, account, password):
        super(ProductData, self).__init__(host=host, account=account, password=password)

    def get_pre_data_by_project_demand_datas(self, all_project_demand_datas):
        pre_insert_data = []
        update_people = '未指定'
        update_time = ''
        for project_id, project_demand_datas in all_project_demand_datas.items():
            for project_demand_id, project_demand_data in project_demand_datas.items():
                if project_demand_data['project_demand_stage'] == '测试完毕':
                    pre_remarks = self.get_project_demand_remark_by_project_demand_id(project_demand_id)
                    for i, pre_remark in pre_remarks.items():
                        if pre_remark.get('update_context_end') == 'tested':
                            update_people = pre_remark.get('update_people')
                            update_time = pre_remark.get('update_time')
                    if update_time and update_time < datetime.datetime.now().strftime("%Y-%m-%d"):
                        continue
                    test_content = 'storyid=' + project_demand_data.get('project_demand_id') + \
                                   '  ' + project_demand_data.get('project_demand_name')
                    pre_time = (CommonTools.get_work_days(datetime.datetime.now() + datetime.timedelta(days=1))).strftime("%Y%m%d")
                    pre_insert_data.append([
                        project_demand_data.get('project_name'),
                        test_content,
                        '通过',
                        update_people,
                        project_demand_data.get('project_demand_create_people'),
                        project_demand_data.get('project_demand_appoint_people'),
                        pre_time,
                    ])
        # if pre_insert_data:
        #     pre_insert_data = list(set(pre_insert_data))
        print(pre_insert_data, '预生产数据')
        return pre_insert_data

    def get_pro_data_by_project_demand_datas(self, all_project_demand_datas):
        """
        通过备注获取上线成功结果信息
        :param all_project_demand_datas:
        :return:
        """
        pro_insert_data = []
        update_people = ''
        test_people = ''
        for project_id, project_demand_datas in all_project_demand_datas.items():
            for project_demand_id, project_demand_data in project_demand_datas.items():
                # 上线成功的需求
                # 昨天时间
                new_pro_time = (datetime.datetime.now()).strftime("%Y-%m-%d")
                pro_time = (CommonTools.get_work_days(datetime.datetime.now() - datetime.timedelta(days=1))).strftime(
                    "%Y-%m-%d")
                test_content = 'storyid=' + project_demand_data.get('project_demand_id') + \
                               '  ' + project_demand_data.get('project_demand_name')
                # 上线成功的情况
                if project_demand_data['project_demand_stage'] == '已发布':
                    pro_remarks = self.get_project_demand_remark_by_project_demand_id(project_demand_id)
                    print(pro_remarks, '已发布')
                    if not pro_remarks:
                        continue
                    end_pro_time = 0
                    for i, pro_remark in pro_remarks.items():
                        if pro_remark.get('update_context_end') == 'released' and pro_remark.get('update_time') >= pro_time:
                            end_pro_time = pro_remark.get('update_time')
                            update_people = pro_remark.get('update_people')
                        if pro_remark.get('update_context_end') == 'tested':
                            test_people = pro_remark.get('update_people')
                    if end_pro_time and update_people:
                        pro_time = (CommonTools.get_work_days(datetime.datetime.now() - datetime.timedelta(days=1))).strftime("%Y-%m-%d")
                        pro_insert_data.append([
                            project_demand_data.get('project_name'),
                            test_content,
                            '通过',
                            test_people if test_people else '未指派',
                            project_demand_data.get('project_demand_create_people'),
                            project_demand_data.get('project_demand_appoint_people'),
                            update_people,
                            pro_time,
                            '上线成功',
                        ])
                # 上线失败的
                # 情况一： 确定无法上线，将状态改为研发中
                # 判断条件： 有过测试状态，且研发中的时间为上线当天修改的
                if project_demand_data['project_demand_stage'] == '研发中':
                    test_people = ''
                    pro_remarks = self.get_project_demand_remark_by_project_demand_id(project_demand_id)
                    if not pro_remarks:
                        continue
                    for i, pro_remark in pro_remarks.items():
                        # 有过测试状态
                        if pro_remark.get('update_context_end') == 'tested' and pro_remark.get('update_time') <= pro_time:
                            test_people = pro_remark.get('update_people')
                        if pro_remark.get('update_context_end') == 'developing':
                            update_people = pro_remark.get('update_people')
                    if test_people:
                        pro_time = (CommonTools.get_work_days(datetime.datetime.now() - datetime.timedelta(days=1))).strftime("%Y-%m-%d")
                        pro_insert_data.append([
                            project_demand_data.get('project_name'),
                            test_content,
                            '通过',
                            test_people if test_people else '未指派',
                            project_demand_data.get('project_demand_create_people'),
                            project_demand_data.get('project_demand_appoint_people'),
                            update_people if update_people else '未指派',
                            pro_time,
                            '上线失败',
                        ])
                # 情况二： 今天没有上线，忘记修改状态
                if project_demand_data['project_demand_stage'] == '测试完毕':
                    test_people = ''
                    pro_remarks = self.get_project_demand_remark_by_project_demand_id(project_demand_id)
                    if not pro_remarks:
                        continue
                    old_time = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d")
                    for i, pro_remark in pro_remarks.items():
                        if pro_remark.get('update_context_end') == 'tested' and pro_remark.get('update_time')\
                                < pro_time and pro_remark.get('update_time') > old_time:
                            test_people = pro_remark.get('update_people')

                    if test_people:
                        pro_time = (CommonTools.get_work_days(datetime.datetime.now() - datetime.timedelta(days=1))).strftime("%Y-%m-%d")
                        pro_insert_data.append([
                            project_demand_data.get('project_name'),
                            test_content,
                            '通过',
                            test_people if test_people else '未指派',
                            project_demand_data.get('project_demand_create_people'),
                            project_demand_data.get('project_demand_appoint_people'),
                            '未指派',
                            pro_time,
                            '上线失败',
                        ])
        print(pro_insert_data, '生产数据')
        return pro_insert_data


class Messenger(object):
    MAIL_SERVICE_URL = r'http://10.13.225.228:8082/api/mail/'

    @classmethod
    def post_email(cls, to, subjects, content, type="6"):
        """
        发送邮件
        """
        print('开始发送邮件')
        try:
            email_body = {"inboxes": to, "subject": subjects, "content": content, "module": "mn_alarm", "type": 6}
            r = requests.post(cls.MAIL_SERVICE_URL, data=json.dumps(email_body))
            r.raise_for_status()
            result = r.json()
            if result['code'] == 0:
                print('send mail to %s OK' % to)
                return 0
            else:
                print('send mail to %s Failed, content =%s, Msg:%s' % (to, content, result))
                return -1
        except Exception as e:
            print('On send mail err occurred:%s' % e)
            return -1


class SendEmail(object):

    @classmethod
    def send_pre_email(cls, pre_insert_datas, receiver_list):
        # 发预上线文档
        for receiver in receiver_list:
            pre_time = datetime.datetime.now() + datetime.timedelta(days=1)
            pre_time = CommonTools.get_work_days(pre_time)
            content_time = pre_time.strftime('%Y年%m月%d日')
            pre_time = pre_time.strftime('%Y%m%d')
            pre_name = '自动发邮件--系统更新--业务平台日常更新[' + str(pre_time) + ']'
            content = """
                   <div style="font-family: 黑体;">
                   <br><br>
                   各位同事：
                   <br><br>
                   大家好，GIC更新，请支持，谢谢~
                   <br><br><br>
                   """
            content += '更新时间' + content_time
            content += """
                   更新方式：日常更新
                   <br>
                   运维人员：郝志新【18910538051】
                   <br><br>
                   请各产品线确认已通过上线评审。
                   <br>
                   请通过测试的产品线统一准备好上线文档，提交应用运维。
                   <br>
                   若产品线有需要追加的任务请负责人回复邮件，谢谢~
                   <br>
                   如有其他异议或疑问请及时回复本邮件。
                   <br>
                   """
            content += '以下是' + pre_time + '上线内容'
            content += """
                   <br>
                   <table border="1" cellspacing="0" width="80%" height="10%" style="margin-top: 30px;
                    border: 1px solid #aaa;" align="left">
                   <tr><th colspan='7'>上线内容测试报告</th></tr>
                   <tr>
                   <th width='10%'>产品线</th>
                   <th width="20%">测试内容</th>
                   <th width="5%">测试结果</th>
                   <th width="8%">测试负责人</th>
                   <th width="8%">产品负责人</th>
                   <th width="8%">研发负责人</th>
                   <th width="5%">版本</th>
                   </tr>
               """
            for pre_insert_data in pre_insert_datas:
                content += """
                       <tr>
                       <td align='center'>{}</td>
                       <td align='center'>{}</td>
                       <td align='center'>{}</td>
                       <td align='center'>{}</td>
                       <td align='center'>{}</td>
                       <td align='center'>{}</td>
                       <td align='center'>{}</td>
                       </tr>
                   """.format(pre_insert_data[0], pre_insert_data[1], pre_insert_data[2],
                              pre_insert_data[3], pre_insert_data[4], pre_insert_data[5],
                              pre_insert_data[6]
                              )
            content += """</div>"""
            subject = pre_name
            a = Messenger()
            a.post_email(receiver, subject, content)

    @classmethod
    def send_pro_email(cls, pro_insert_datas, receiver_list):
        for receiver in receiver_list:
            # 发上线文档
            pro_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
            content_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y年%m月%d日')
            pro_name = 'RE：自动发邮件--系统更新结果--业务平台日常更新结果[' + str(pro_time) + ']'
            content = """
                       <div style="font-family: 黑体;">
                       <br><br><strong>
                       各位同事：
                       <br>
                       大家好，昨日上线结果如下：
                       <br>
                       """
            content += '以下是' + content_time + '上线内容'
            content += """
                       </strong>
                       <br>
                       <table border="2" cellspacing="0" width="80%" height="10%" style="margin-top: 30px" align="left">
                       <tr><th colspan='9'>上线内容测试结果报告</th></tr>
                       <tr height='3%',class='tabletitle'>
                       <th width='10%'>产品线</th>
                       <th width="20%">测试内容</th>
                       <th width="5%">测试结果</th>
                       <th width="8%">测试负责人</th>
                       <th width="8%">产品负责人</th>
                       <th width="8%">研发负责人</th>
                       <th width="8%">上线负责人</th>
                       <th width="5%">上线时间</th>
                       <th width="5%">上线结果</th>
                       </tr>
                   """
            for pro_insert_data in pro_insert_datas:
                content += """
                           <tr>
                           <td height='10%'align='center'>{}</td>
                           <td height='10%'align='center'>{}</td>
                           <td height='10%'align='center'>{}</td>
                           <td height='10%'align='center'>{}</td>
                           <td height='10%'align='center'>{}</td>
                           <td height='10%'align='center'>{}</td>
                           <td height='10%'align='center'>{}</td>
                           <td height='10%'align='center'>{}</td>
                           <td height='10%'align='center'>{}</td>
                           </tr>
                       """.format(pro_insert_data[0], pro_insert_data[1], pro_insert_data[2],
                                  pro_insert_data[3], pro_insert_data[4], pro_insert_data[5],
                                  pro_insert_data[6], pro_insert_data[7], pro_insert_data[8]
                                  )
            content += """</div>"""
            subject = pro_name
            a = Messenger()
            a.post_email(receiver, subject, content)


class CommonTools(object):
    @classmethod
    def get_work_days(cls, old_time):
        """
        获取非工作日的日期
        :param old_time:
        :return:
        """
        while True:
            if is_workday(old_time):
                break
            old_time = old_time + datetime.timedelta(days=1)
        return old_time


# 设置禅道的账号和密码
zentao_account = "jinzn"
zentao_password = "zaq123edc"

# 爬虫获取数据
logging.info('我来啦')
zentao_host = "http://cds-cdproject.capitalonline.net"
test_object = ProductData(host=zentao_host, account=zentao_account, password=zentao_password)
# 获取所有的项目id号
project_ids = test_object.get_project_ids()
# 获取所有条件齐全的项目需求信息
all_project_demand_datas = test_object.get_project_demand_by_project_ids(project_ids)


# 设置收件人的邮箱
receiver_list = ['zening.jin@capitalonline.net', 'jing1.zhang@capitalonline.net', 'jing.zhang2@capitalonline.net',
                 'yanwei.xia@capitalonline.net', 'tao.xu@capitalonline.net']
receiver_list = ['zening.jin@capitalonline.net']

if __name__ == '__main__':
    # 发送上线结果文档
    pro_insert_data = test_object.get_pro_data_by_project_demand_datas(all_project_demand_datas)
    SendEmail.send_pro_email(pro_insert_data, receiver_list)



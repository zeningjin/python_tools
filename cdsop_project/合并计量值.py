# -*- coding: utf-8 -*-
# @Time    : 2020/10/9 下午2:45
# @Author  : jinzening
# @File    : 合并计量值.py
# @Software: PyCharm

import datetime
import time
from pymongo import MongoClient

MONGO_DB_HOST = '172.20.3.35'
MONGO_DB_PORT = 27017
MONGO_STR = 'mongodb://%s:%s' % (MONGO_DB_HOST, MONGO_DB_PORT)
MONGO_DB_TELEMETRY_NAME = 'cds_telemetry_monitor'
COLLECTION_TELEMETRY_FLOW = 'flow_data'
#　测试
MONGO_DB_TELEMETRY_NAME = 'flow_snmp'
COLLECTION_TELEMETRY_FLOW = 'flow_data'
# 新建的表格
NEW_TELEMETRY_FLOW = 'flow_data_5min'
client = MongoClient(MONGO_STR)
db = client[MONGO_DB_TELEMETRY_NAME]
# 当前时间
NOW = datetime.datetime.now()

def insert_flow_data(insert_data):
    """
    插入新的表格中
    :param insert_data:
    :return:
    """
    db[NEW_TELEMETRY_FLOW].insert(insert_data)
    print('插入成功')


def get_flow_data(res_object, start_time=''):
    """
    将数据拼接起来
    :param res_object:
    :param start_time:
    :return:
    """
    flow_data = [{
        'pipe_id': flow.get('_id'),
        "in_bps": flow.get("in_bps"),
        "out_bps": flow.get("out_bps"),
        'time': flow.get('time') if flow.get('time') else start_time
    } for flow in res_object]
    return flow_data


def aggregate_telemetry():
    """
    将telemetry流量进行聚合
    :return:
    """
    # start_time = datetime.datetime(2020, 9, 22, 10, 3, 36)
    # end_time = datetime.datetime(2020, 9, 22, 10, 8, 36)
    start_time = datetime.datetime(2020, 2, 21, 00, 00, 00)
    end_time = datetime.datetime(2020, 10, 9, 11, 2, 00)
    while True:
        # now减去10分钟，是为了防止数据不全造成的结果不准确
        if end_time >= NOW - datetime.timedelta(minutes=10):
            # 为程序无限跑带来了可能，否则，一直跑太浪费资源
            time.sleep(200)
            break
        query = {
            'time': {'$gt': start_time, '$lt': end_time}
        }
        # 分组求和
        new_flow_datas = db[COLLECTION_TELEMETRY_FLOW].aggregate([
            {'$match': query},
            {'$group':
                {'_id': "$pipe_id", 'in_bps': {'$avg': "$in_bps"}, 'out_bps': {'$avg': "$out_bps"}}}
        ])
        # 将查询到的数据转为字典格式
        new_flow_data = get_flow_data(new_flow_datas, start_time)
        print(new_flow_data)
        if new_flow_datas:
            # 数据插入
            insert_flow_data(new_flow_data)
            print(new_flow_data)
        start_time += datetime.timedelta(minutes=5)
        end_time += datetime.timedelta(minutes=5)
    return new_flow_datas


if __name__ == '__main__':
    aggregate_telemetry()
    # insert(new_flow_datas)




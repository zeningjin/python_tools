# -*- coding: utf-8 -*-
# @Time:    19-12-12 下午6:04

import datetime
import random
from pymongo import MongoClient

# MONGO_DB_HOST = '10.2.13.32'
MONGO_DB_HOST = '172.20.3.35'
MONGO_DB_PORT = 27017
MONGO_STR = 'mongodb://%s:%s' % (MONGO_DB_HOST, MONGO_DB_PORT)
MONGO_DB_NAME_5m = 'flow_snmp'
COLLECTION_FLOW_5m = 'flow_data_test'
MONGO_DB_NAME_30s = 'flow_mete'
COLLECTION_FLOW_30s = 'flow_data_1m'
MONGO_DB_TELEMETRY_NAME = 'cds_telemetry_monitor'
COLLECTION_TELEMETRY_FLOW = 'flow_data'

client = MongoClient(MONGO_STR)
# db = client[MONGO_DB_NAME_5m]
db = client[MONGO_DB_TELEMETRY_NAME]
COLLECTION_TELEMETRY_FLOW = 'flow_data'

pipe_id = '0a2a2f36-dd33-11ea-8e8f-0afe0edda181'

time = datetime.datetime(2020, 9, 10, 19, 27, 0)
end_time = datetime.datetime(2020, 9, 20, 23, 00, 0)


def insert():
    global time
    global end_time
    insert_data = []
    while time < end_time:
        insert_data.append({
            'pipe_id': pipe_id,
            'time': time,
            'in_flow': random.randint(1314, 3304),
            'out_flow': random.randint(1314, 3304),
            'in_bps': random.randint(1314, 3304),
            'out_bps': random.randint(1314, 3304)
        })
        # time += datetime.timedelta(minutes=10)
        time += datetime.timedelta(seconds=30)
    # insert_flow = db[COLLECTION_FLOW_5m].insert(insert_data)
    insert_flow = db[COLLECTION_TELEMETRY_FLOW].insert(insert_data)

    print(insert_flow)


def delete():
    col = db[COLLECTION_FLOW_5m]
    query = {'pipe_id':'649692fe-b932-11ea-af06-a62ad09b0d84'}
    res = col.delete_many(query)
    print(res.deleted_count)


def find():
    pipe_id = '649692fe-b932-11ea-af06-a62ad09b0d84'
    now = datetime.datetime.now()
    lasttime = now - datetime.timedelta(hours=4)
    col = db[COLLECTION_FLOW_5m]
    query = {
        'pipe_id': pipe_id,
        'time': {'$gt': lasttime, '$lt': now}
    }
    docs = col.find(query)
    print(docs.count())
    return docs


if __name__ == '__main__':
    insert()
    #delete()

#!usr/bin/env python
# encoding:utf-8
from __future__ import division

from kafka import KafkaConsumer

# 生成生产者对象 bootstrap_servers写入kafka的地址
consumer = KafkaConsumer('devtest-topic', bootstrap_servers=['140.210.66.34:9093'])

# 读取消息
for msg in consumer:
    info = "%s:%d:%d: key=%s  value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
    print(info)

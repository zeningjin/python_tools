#!usr/bin/env python
# encoding:utf-8
from __future__ import division

from kafka import KafkaConsumer, TopicPartition
from concurrent.futures import ThreadPoolExecutor

# 生成生产者对象 bootstrap_servers写入kafka的地址

topic = 'devtest-topic'
consumer = KafkaConsumer(topic, bootstrap_servers=['140.210.66.34:9093'])

parts = consumer.partitions_for_topic(topic)
print("所有的分区获取成功", parts)

#
# consumer.assign([tp])

# 指定offset为最近可用的offset
# consumer.seek_to_end()

# 读取消息
for msg in consumer:

    info = "%s:%d:%d: key=%s  value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
    print(info, type(info))


#!usr/bin/env python
# encoding:utf-8
from __future__ import division

# pip install kafka-python
from kafka import KafkaConsumer, KafkaProducer

# 生成生产者对象 bootstrap_servers写入kafka的地址
# kafka的配置文件中需要写入外部访问地址 advertised.listeners=PLAINTEXT://140.210.66.34:9092
producer = KafkaProducer(bootstrap_servers='140.210.66.34:9093')

# 发送消息 第一位参数为主题名称 partition指定分区
future = producer.send('devtest-topic', key=b'my_key', value=b'my_value', partition=0)

# 验证
record_metadata = future.get(timeout=10)
print("future对象:", record_metadata)
print("======================================================")
print("接收的topic:", record_metadata.topic)
print("partition_ID:", record_metadata.partition)
print("offset:", record_metadata.offset)
print("==========发送成功============")

# 关闭生产者
producer.close()
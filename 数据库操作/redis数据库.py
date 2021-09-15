import redis   #导入redis模块

# 建议使用以下连接池的方式
# 设置decode_responses=True，写入的KV对中的V为string类型，不加则写入的为字节类型。
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, decode_responses=True)
rs = redis.Redis(connection_pool=pool)

# key="color",value="red"，设置过期时间5秒
rs.set('color', 'red', ex=5)

# 与rs.set('color', 'red', ex=5)相同
rs.setex('color', 5, 'red')

# 打印获取color键对应的值，超时后获取值为None
print(rs.get('color'))

# 如果color存在输出None，如果不存在，则输出True
print(rs.set('color', 'green', nx=True))

# 如果color存在输出True，如果不存在，则输出None
print(rs.set('color', 'yellow', xx=True))

# 批量赋值
rs.mset({'key1':'value1', 'key2':'value2', 'key3':'value3'})

# 批量获取值
rs.mget('key1', 'key2', 'key3')

# 设置新值为blue，同时返回设置前的值
print(rs.getset('color', 'blue'))

rs.set('lang', 'Chinese')


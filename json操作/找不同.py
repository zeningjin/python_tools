json_one = {}
json_two = {}


def cmp(json_one, json_two, thiskey='最外层'):
    # 字典格式
    if isinstance(json_one, dict):
        count = 0
        for key in json_one:
            # 先比较两个json串的健
            if key not in json_two:
                print('json_two的', thiskey, '的', key, '这个健不存在')
        for key in json_two:
            if key in json_one:
                thiskey = key
                cmp(json_one[key], json_two[key], thiskey)
    # 字符串格式
    elif isinstance(json_one, list):
        if len(json_one) != len(json_two):
            print(thiskey, "这个健的列表不同: '{}' != '{}'".format(json_one, json_two))
        for json_one, json_two in zip(json_one, json_two):
            cmp(json_one, json_two, thiskey)
    else:
        if str(json_one) != str(json_two):
            print(thiskey, '的', json_one, '!=', json_two)


cmp(json_one, json_two)
print('*********************************')
cmp(json_two, json_one)

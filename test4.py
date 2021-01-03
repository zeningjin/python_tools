def get_split_params(tpl, global_params, local_params):
    stack = [(tpl, k) for k in tpl.keys()]
    while stack:
        d, k = stack.pop()
        if k in local_params or k in global_params:
            d[k] = local_params.get(
                k) if k in local_params else global_params.get(k)
            print(d)
            continue
        if isinstance(d[k], dict):
            stack.extend([(d[k], key) for key in d[k].keys()])
        else:
            val = local_params.get(
                k) if k in local_params else global_params.get(k)
            if val:
                d[k] = val
    return tpl

tpl = {"customer_id":"","site_id":"","app_type":"","project_id":""}
global_params = {"area_id": "CN", "app_name": "wang12", "task_id": "31f70f8c-4045-11eb-90c3-1223f8fcca0d", "pubnet": {}, "pub_goods_id": None, "site_id": "25c7978e-c820-4cd6-8bd3-77f90e410ffb", "app_id": "287b469b-c0dd-48e0-9889-0c482a46ae2b", "private": [], "new_gic_flag": 1, "operation_id": 10923775, "project_id": "43943f61-299f-11eb-9bf2-e4029b522ee7", "customer_id": "E1018711", "data": None, "user_from": "console-end", "customer_user_id": "628448", "__gic_id": None}
local_params = {"task_type": "OrderCreateApp", "task_id": "31fac8fc-4045-11eb-90c3-1223f8fcca0d"}

global_params.update(local_params)
print(1111, global_params)
result = get_split_params(tpl, global_params, local_params)
print(result)

dict.fromkeys(x for x in local_params if x in global_params)

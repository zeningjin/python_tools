json_one = {"username": "root", "windows_activation": None, "area_id": "CN", "description": "video.api.mama.cn", "cache_uid": "", "count_num": 1, "ram": 2, "site_id": "25c7978e-c820-4cd6-8bd3-77f90e410ffb", "app_id": "17c04d9b-d6ed-4824-a680-b2ca093cc50c", "description_num": "", "dedicated_id": "", "ext_disks": [], "new_gic_flag": 1, "vm_public_key": "", "password": "Abcd_1234", "nets": [[{"ipv6_bind": None, "pipe_id": "ee1547ce-ee88-11ea-9e4c-665c3623d5b8", "ip": "166.166.14.194", "mask": 30, "dns": "", "gate": "166.166.14.193"}]], "user_from": "unknown", "small_cpu_limit_factor": 1.0, "selinux_flag": False, "task_type": "orderCreateVM", "vpc_net_flag": "", "base_vm_id": "", "goods_id": 4505, "os_template_id": "004ca86a-d281-46ae-bf65-812fd8f588c6", "vm_family_id": "c46782be-cde0-11e7-af38-0242ac110d06", "tpl_disks": [], "utc_flag": False, "vm_type_id": "146468f2-c413-4fdd-bf5c-bcf59e976898", "vm_attr_values": [], "vm_ids": ["5e538ac5-329c-448f-8277-9b3111bdc50f"], "cpu_type": "cpu_normal", "isolate_group_id": "", "sub_order_id": {"vm_order_id": "889c5530-2192-11eb-bf51-c85b76d6be67"}, "cpu": 2, "system_disk": {"size": 60, "type": "system_disk", "iops": 0, "disk_id": "91a4e9c8-c365-11e7-99f7-c85b76ac066e", "iops_base": 600, "disk_type": "system_disk", "iops_pkg": 0, "mbps_base": 64, "iops_size": 600}, "flavor_id": ""}
json_two = {"username": "root", "windows_activation": None, "area_id": "CN", "description": "video.api.mama.cn", "cache_uid": "", "count_num": 1, "ram": 2, "site_id": "25c7978e-c820-4cd6-8bd3-77f90e410ffb", "app_id": "17c04d9b-d6ed-4824-a680-b2ca093cc50c", "description_num": "", "dedicated_id": "", "ext_disks": [], "new_gic_flag": 1, "vm_public_key": "", "password": "Abcd_1234", "nets": [[{"ipv6_bind": None, "pipe_id": "ee1547ce-ee88-11ea-9e4c-665c3623d5b8", "ip": "166.166.14.194", "mask": 30, "dns": "", "gate": "166.166.14.193"}]], "user_from": "unknown", "small_cpu_limit_factor": 1.0, "selinux_flag": False, "task_type": "orderCreateVM", "vpc_net_flag": "", "base_vm_id": "", "goods_id": 4505, "os_template_id": "004ca86a-d281-46ae-bf65-812fd8f588c6", "vm_family_id": "c46782be-cde0-11e7-af38-0242ac110d06", "tpl_disks": [], "utc_flag": False, "vm_type_id": "146468f2-c413-4fdd-bf5c-bcf59e976898", "vm_attr_values": [], "vm_ids": ["7c94d134-2744-41fe-88b1-73bad1e6414f"], "cpu_type": "cpu_normal", "isolate_group_id": "", "sub_order_id": {"vm_order_id": "9dc9d88a-218b-11eb-bf51-c85b76d6be67"}, "cpu": 2, "system_disk": {"size": 60, "type": "system_disk", "iops": 0, "disk_id": "91a4e9c8-c365-11e7-99f7-c85b76ac066e", "iops_base": 600, "disk_type": "system_disk", "iops_pkg": 0, "mbps_base": 64, "iops_size": 600}, "flavor_id": ""}
def cmp(json_one,json_two,thiskey='最外层'):
    #字典格式
    if isinstance(json_one, dict):
        count=0
        for key in json_one:
            # 先比较两个json串的健
            if key not in json_two:
                print('json_two的',thiskey,'的',key,'这个健不存在')
        for key in json_two:
            if key in json_one:
                thiskey=key
                cmp(json_one[key],json_two[key],thiskey)
    #字符串格式
    elif isinstance(json_one, list):
        if len(json_one) != len(json_two):
            print(thiskey,"这个健的列表不同: '{}' != '{}'".format(json_one, json_two))
        for json_one,json_two in zip(json_one,json_two):
            cmp(json_one,json_two,thiskey)
    else:
        if str(json_one) != str(json_two):
            print(thiskey,'的',json_one,'!=',json_two)
cmp(json_one,json_two)
print('*********************************')
cmp(json_two,json_one)
# cmp(dict1,dict2)

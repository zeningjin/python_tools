def get_os_and_disk_info_by_vm_ids(self,vm_ids):
    vm_dicts = {}
    # for v in vms:
    #     vm_dicts[v.get('id')] = v
    # if vm_params.get('disk_flag'):
    #     self.get_vm_disk_info(vm_dicts)
    for vm_id in vm_ids:
        vm_dicts[vm_id]={}
    self.get_vm_disk_info(vm_dicts)
    data = []

    vm_type_family = {
        'cpu_io': u'IO增强型',
        'cpu_high': u'高性能类型族',
        'cpu_normal': u'标准型类型族'
    }

    disk_type_dict = {
        'ssd_disk': u'超高性能型云硬盘（SSD）',
        'high_disk': u'高性能型硬盘',
        'big_disk': u'大容量硬盘'
    }
    c
    for vm in vms:
        os_id_list.append(vm.get('os__id'))
        for d in vm.get('disks', []):
            disk_type_list.append(d.get('disk_type'))

    disk_type_list = list(set(disk_type_list))
    os_id_list = list(set(os_id_list))
    os_obj_list = cloud_models.OsSite.objects.filter(os_id__in=os_id_list)
    map(lambda x: os_obj_dict.update({x.os_id: x}), os_obj_list)
    basic_vm_disk = basic_models.BasicVMDisk.objects.filter(attr__key__in=disk_type_list,
                                                            is_valid=1)
    logger.info(basic_vm_disk)
    map(lambda x: basic_vm_disk_dict.update({x.attr.key: x}), basic_vm_disk)
    data=[]
    for vm in vms:
        vm_info={}
        if vm_params.get('disk_flag'):
            # disks = vm.disks if hasattr(vm, 'disks') else []
            disks = vm.get('disks', [])
            disk_info = {
                'auth_total_disk_size': self.auth_operation.max_attach_disk_num if vm.get(
                    "cpu_type") != 'lxc' else 8
            }
            system_iops_size = 600
            if vm_type:

                system_disk_name = vm_type.get('vm_family__basic_disk__name')
                if settings.LANGUAGE_CODE == 'en':
                    system_disk_name = vm_type.get('vm_family__basic_disk__name_en')
                system_disk_name = _(u'系统盘') + u'(' + system_disk_name + u')'
                system_iops_size = int(vm_type.get('vm_family__basic_disk__iops') or 0)
            else:
                system_disk_name = u'系统盘(超高性能型(SSD))' if vm.get('cpu_type') == 'cpu_io' else u'系统盘(性能型)'
            os_obj = os_obj_dict.get(vm.get('os__id'))
            attach_size = 0
            if os_obj:
                if os_obj.tpl_disks:
                    if json.loads(os_obj.tpl_disks).get('disks'):
                        for os in json.loads(os_obj.tpl_disks).get('disks'):
                            attach_size += int(os.get('size'))
            disk_info['system'] = {
                'disk_type_name': system_disk_name,
                'size': int(vm.get('os__template_size')) - attach_size,
                'iops_size': system_iops_size
            }
            attach = []
            for d in disks:
                attach_disk_info = {
                    'disk_type': d.get('disk_type'),
                    'disk_id': d.get('disk_id'),
                    'size': d.get('size'),
                    'iops': d.get('iops_num'),
                    'iops_size': d.get('iops_size'),
                    'disk_uuid': d.get('disk_uuid'),
                    'disk_label': d.get('label')
                }
                basic_vm_disk = basic_vm_disk_dict.get(d.get('disk_type'))
                # basic_vm_disk = basic_models.BasicVMDisk.objects.filter(attr__key=d.get('disk_type'),
                #                                                         is_valid=1).first()
                if basic_vm_disk:
                    attach_disk_info['disk_type_name'] = basic_vm_disk.name
                    attach_disk_info['has_iops'] = int(basic_vm_disk.is_package)
                else:
                    attach_disk_info['disk_type_name'] = disk_type_dict.get(d.get('disk_type'))
                    attach_disk_info['has_iops'] = 1 if d.get('disk_type') == 'ssd_disk' else 0
                attach.append(attach_disk_info)
            disk_info['attach'] = attach
            vm_info['disks'] = disk_info
        data.append(vm_info)
    total = len(vms)
    # res_data = {'total': len(data), 'list': data}
    if vm_params['page_flag']:
        res_data = {'total': total, 'list': data}
        return CommonReturn(CodeMsg.SUCCESS, 'success', res_data)
    return CommonReturn(CodeMsg.SUCCESS, 'success', data)

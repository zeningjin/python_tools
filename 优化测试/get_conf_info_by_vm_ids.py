def get_conf_info_by_vm_ids(vms):
    vm_type = basic_models.VMType.objects.select_related('vm_family').filter(
        is_valid=1).values('name',
                           'name_en',
                           'conf_id',
                           'vm_family_id',
                           'vm_family__name',
                           'vm_family__name_en',
                           'vm_family__basic_disk__name',
                           'vm_family__basic_disk__name_en',
                           'vm_family__basic_disk__iops',
                           'vm_family__architect_name',
                           'vm_family__architect_type')
    vm_type_dict = {}
    map(lambda x: vm_type_dict.update({x.get('conf_id'): {
        'vm_family_id': x.get('vm_family_id'),
        'name': x.get('name'),
        'name_en': x.get('name_en'),
        'vm_family_name': x.get('vm_family__name'),
        'vm_family_name_en': x.get('vm_family__name_en'),
        'vm_family__basic_disk__name': x.get("vm_family__basic_disk__name"),
        'vm_family__basic_disk__name_en': x.get("vm_family__basic_disk__name_en"),
        'vm_family__basic_disk__iops': x.get("vm_family__basic_disk__iops"),
        'vm_family__architect_name': x.get("vm_family__architect_name"),
        'vm_family__architect_type': x.get("vm_family__architect_type")
    }}), vm_type)
    data=[]
    for vm in vms:
        vm_info={}
        vm_type = None
        if vm_type_dict.get(vm_info.get('conf_id')):
            vm_type = vm_type_dict[vm_info.get('conf_id')]
            vm_info['vm_family_id'] = vm_type.get('vm_family_id')
            vm_info['vm_family_name'] = vm_type.get('vm_family_name')
            vm_info['vm_type_name'] = vm_type.get('name')

            vm_info['architect_type'] = vm_type.get("vm_family__architect_type")
            vm_info['architect_display_name'] = ARCHITECT_DISPLAY_NAME.get(
                vm_type.get("vm_family__architect_name")).get("name")
            if settings.LANGUAGE_CODE == 'en':
                vm_info['vm_type_name'] = vm_type.get('name_en')
                vm_info['vm_family_name'] = vm_type.get('vm_family_name_en')
        else:
            vm_info['vm_family_id'] = ''
            vm_info['vm_family_name'] = vm_type_family.get(vm.get('cpu_type'))
            vm_info['vm_type_name'] = vm.get('goods__product_conf__name')
        data.append(vm_info)
    total = len(vms)
    # res_data = {'total': len(data), 'list': data}
    if vm_params['page_flag']:
        res_data = {'total': total, 'list': data}
        return CommonReturn(CodeMsg.SUCCESS, 'success', res_data)
    return CommonReturn(CodeMsg.SUCCESS, 'success', data)

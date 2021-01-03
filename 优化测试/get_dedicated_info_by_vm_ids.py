def get_dedicated_info_by_vm_ids(vms):
    for vm in vms:
        label_ids = []
        if vm.get('vm_label_ids'):
            label_ids = vm.get('vm_label_ids').split(',')
        vm.update({'label_ids': label_ids})
        # vm_all_label_ids.update(label_ids)

    customer_vm_labels = cloud_models.VMLabel.objects.filter(is_valid=1).values('id', 'name')
    vm_label_dict = {}
    map(lambda x: vm_label_dict.update({str(x.get('id')): x.get('name')}), customer_vm_labels)

    vm_status_dict = {}
    map(lambda x: vm_status_dict.update({x[0]: x[1]}), cloud_models.VM.VM_STATUS)

    tools_status_dict = {}
    map(lambda x: tools_status_dict.update({x[0]: x[1]}), cloud_models.VM.TOOLS_STATUS)

    kvm_ids = [{'id': v.get('id'), 'site_id': v.get('app__site_id')} for v in vms if v.get('vm_type') == 'kvm']
    kvm_status_data = {}
    if kvm_ids:
        kvm_service = KVMService(self.customer, self.user)
        kvm_status_data = kvm_service.get_kvm_status(kvm_ids)

    dedicates = cloud_models.Dedicated.objects.filter(customer_id=self.customer_id,
                                                      is_valid=1).values(
        'id',
        'name',
        'pipe_id'
    )
    dedicated_dict = {}
    map(lambda x: dedicated_dict.update({x.get('id'): x.get('name')}), dedicates)
    dedicated_pipe_dict = {}
    map(lambda x: dedicated_pipe_dict.update({x.get('pipe_id'): x}), dedicates)
    data=[]
    for vm in vms:
        vm_status_str = vm_status_dict.get(vm.get("status"), _(u'未知'))
        if vm.get("status") == 'creating':
            vm_status_str = "创建" + str(vm.get("processing", 0)) + "%"
        vm_info={
            'vm_status_str': vm_status_str
        }
    for vm in vms:
        vm_info={}
        if vm.get('dedicated_id'):
            vm_info['dedicated_name'] = dedicated_dict.get(vm.get('dedicated_id'), '')
            vm_info['dedicated_id'] = vm.get('dedicated_id')
        if vm_info.get('type') == 'kvm':
            kvm_status = kvm_status_data.get(vm_info.get('vm_id'), vm_info['vm_status'])
            vm_info['vm_status_str'] = vm_status_dict.get(kvm_status, u'未知')
            if kvm_status == 'creating':
                vm_status_str = "创建" + str(vm.get("processing", 0)) + "%"
                vm_info['vm_status_str'] = vm_status_str
            vm_info['vm_status'] = kvm_status
        vm_label_name = [{
            'id': vm_label_id,
            'name': vm_label_dict.get(vm_label_id)
        } for vm_label_id in vm.get('label_ids') if vm_label_id in vm_label_dict]
        vm_label_name.sort(key=lambda x: x.get("id"), reverse=False)
        vm_info['tags'] = vm_label_name
        data.append(vm_info)
    total = len(vms)
    # res_data = {'total': len(data), 'list': data}
    if vm_params['page_flag']:
        res_data = {'total': total, 'list': data}
        return CommonReturn(CodeMsg.SUCCESS, 'success', res_data)
    return CommonReturn(CodeMsg.SUCCESS, 'success', data)

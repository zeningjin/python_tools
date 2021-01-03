def get_vm_bill_by_vm_ids(self,vm_params):
    data=[]
    for vm in vm_params:
        result={}
        vm_info={}
        # vm_bill_info = vm.bill_info if hasattr(vm, 'bill_info') else {}
        vm_bill_info = vm.get('bill_info', {})
        bill_info = {
            'suborder_id': vm_bill_info.get('suborder_id', ''),
            'bill_method': vm_bill_info.get('bill_method', '0'),
            'bill_status': vm_bill_info.get('bill_status', 1),
            'bill_status_str': vm_bill_info.get('bill_status_str', _(u'正常')),
            'is_auto_renewal': vm_bill_info.get('is_auto_renewal', 1),
            'bill_duration': vm_bill_info.get('renewal_value', 0),
            'renewal_bill_duration': vm_bill_info.get('renewal_bill_duration', 0),
            'renewal_bill_method': vm_bill_info.get('renewal_bill_method', '0'),
        }
        if vm_bill_info.get('end_bill_time'):
            bill_info['end_bill_time'] = vm_bill_info.get('end_bill_time').strftime('%Y-%m-%d %H:%M:%S')
            bill_info['date_end_bill_time'] = vm_bill_info.get('end_bill_time').strftime('%Y-%m-%d %H:%M:%S')
        else:
            bill_info['end_bill_time'] = u'2099-01-01 00:00:00'
            bill_info['date_end_bill_time'] = u'2099-01-01 00:00:00'
        vm_info['bill_info'] = bill_info
        if vm_bill_info.get('bill_status') in (3, 4, 5, 6):
            vm_info['vm_status_str'] = _(u'等待删除')
            vm_info['vm_status'] = 'down'
        result[vm.get("vm_id")]=vm_info
        data.append(vm_info)
        total = len(vm_params)
        # res_data = {'total': len(data), 'list': data}
    if vm_params['page_flag']:
        res_data = {'total': total, 'list': data}
        return CommonReturn(CodeMsg.SUCCESS, 'success', res_data)
    return CommonReturn(CodeMsg.SUCCESS, 'success', data)
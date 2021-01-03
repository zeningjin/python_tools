def get_private_info_by_vm_ids(vms,vm_params):
    pri_pipe_id_list = []
    for vm in vms:
        for c in vm.get('card_info', []):
            if c.get('pipe_type') == 'private':
                pri_pipe_id_list.append(c.get('pipe_id'))
    gpn_data_dict = {}
    if vm_params.get('pri_flag'):
        gpn_data_list = cloud_models.GICAppNetwork.objects.select_related('gic'). \
            filter(gic__customer_id=self.customer_id,
                   gic__is_valid=1,
                   pipe_id__in=pri_pipe_id_list,
                   is_valid=1).values('gic__gpn_name', 'gic__id', 'pipe_id')
        map(lambda x: gpn_data_dict.update({x.get('pipe_id'): x}), gpn_data_list)
    data=[]
    for vm in vms:
        vm_info={}
        if vm_params.get('pri_flag'):
            # cards = vm.card_info if hasattr(vm, 'card_info') else []
            cards = vm.get('card_info', [])
            pri_info = []
            for c in cards:
                if c.get('pipe_type') == 'private':
                    gpn_data = gpn_data_dict.get(c.get('pipe_id'))
                    pipe_dic = {
                        'card_id': c.get('card_id'),
                        'ip': c.get('ip'),
                        "pipe_type": c.get("pipe__pipe_type") if c.get("pipe__pipe_type") else c.get('pipe_type'),
                        'pipe_id': c.get('pipe_id'),
                        'mac': c.get('mac'),
                        'pipe_name': c.get('pipe_name'),
                        'connected': c.get('connect'),
                        'join_gpn': {"gpn_name": gpn_data.get("gic__gpn_name"),
                                     "gpn_id": gpn_data.get("gic__id")} if gpn_data else None
                    }
                    if c.get('pipe_id') in dedicated_pipe_dict:
                        dec = dedicated_pipe_dict.get(c.get('pipe_id'))
                        pipe_dic['dedicated_data'] = {
                            "id": dec.get('id'),
                            "name": dec.get('name')
                        }
                    pri_info.append(pipe_dic)

            vm_info['pri_info'] = pri_info
        data.append(vm_info)
    total = len(vms)
    # res_data = {'total': len(data), 'list': data}
    if vm_params['page_flag']:
        res_data = {'total': total, 'list': data}
        return CommonReturn(CodeMsg.SUCCESS, 'success', res_data)
    return CommonReturn(CodeMsg.SUCCESS, 'success', data)
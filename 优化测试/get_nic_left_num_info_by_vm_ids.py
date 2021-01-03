def get_nic_left_num_info_by_vm_ids(vms,vm_params):
    pipe_obj_dict = {}
    pub_pipe_dict = {}
    vm_nic_dict = {}
    if vm_params.get('nic_left_flag'):
        app_ids = [vm.get('app_id') for vm in vms]
        app_type = [vm.get('app__type') for vm in vms]
        app_ids = list(set(app_ids))
        if "VPC" in app_type:
            pipe_objs = cloud_models.Pipe.objects.filter(app_id__in=app_ids, type__in=['private', 'public'],
                                                         is_valid=1, pipe_type='vpc_vlan').values('id')
            pipe_obj_counts = cloud_models.Pipe.objects.filter(app_id__in=app_ids, type__in=['private'],
                                                               is_valid=1, pipe_type='vpc_vlan').values(
                'app_id').annotate(
                pipe_count=Count('app_id'))
        else:
            pipe_objs = cloud_models.Pipe.objects.filter(app_id__in=app_ids, type__in=['private', 'public'],
                                                         is_valid=1).values('id')
            pipe_obj_counts = cloud_models.Pipe.objects.filter(app_id__in=app_ids, type__in=['private', 'public'],
                                                               is_valid=1).values('app_id').annotate(
                pipe_count=Count('app_id'))

        map(lambda x: pipe_obj_dict.update({x.get('app_id'): x.get('pipe_count')}), pipe_obj_counts)
        pipe_obj_list = [pipe_obj.get('id') for pipe_obj in pipe_objs]
        pub_pipe_objs = cloud_models.Pipe.objects.filter(app_id__in=app_ids, type='public',
                                                         is_valid=1).values('app_id').annotate(
            pub_pipe_count=Count('app_id'))

        map(lambda x: pub_pipe_dict.update({x.get('app_id'): x.get('pub_pipe_count')}), pub_pipe_objs)
        vm_nic_objs = cloud_models.VMNetworkCard.objects.filter(pipe_id__in=pipe_obj_list).values('vm_id').annotate(
            vm_nic_count=Count('vm_id'))

        map(lambda x: vm_nic_dict.update({x.get('vm_id'): x.get('vm_nic_count')}), vm_nic_objs)
        data=[]
        for vm in vms:
            vm_info = {}
            if vm_params.get('nic_left_flag'):
                # 加参数：本服务器还有多少网络未添加网卡
                nic_num = 0
                pipe_num = pipe_obj_dict.get(vm.get('app_id'), 0)
                pub_pipe_num = pub_pipe_dict.get(vm.get('app_id'), 0)
                logger.info('pipe_num: %s' % pipe_num)
                if pipe_num:
                    nic_num = vm_nic_dict.get(vm.get('id'), 0)

                    logger.info('pipe_num: %s, nic_num: %s' % (pipe_num, nic_num))
                if pub_pipe_num:
                    # 多个公网存在只允许添加一块公网网卡
                    from orm.account import models as account_models
                    user = account_models.CustomerUser.objects.get(id=vm_params.get('user_id'))
                    # 多网卡权限正常展示
                    vm_auth_operation = VMAuthOperation(None, user.customer, user, None, None, None)
                    vm_multi_pub_pipe = vm_auth_operation.multi_pub_pipe
                    if vm_multi_pub_pipe:
                        nic_left_num = pipe_num - nic_num
                    else:
                        nic_left_num = 1 if pipe_num - nic_num > 0 else 0
                else:
                    nic_left_num = pipe_num - nic_num
                vm_info['nic_left_num'] = nic_left_num
            data.append(vm_info)
        total = len(vms)
        # res_data = {'total': len(data), 'list': data}
        if vm_params['page_flag']:
            res_data = {'total': total, 'list': data}
            return CommonReturn(CodeMsg.SUCCESS, 'success', res_data)
        return CommonReturn(CodeMsg.SUCCESS, 'success', data)

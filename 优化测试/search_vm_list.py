def search_vm_list(self, vm_params):
    vm_params['customer_id'] = self.customer_id
    vm_params['user_id'] = self.user_id
    for time_param in ('create_time_from', 'create_time_to', 'end_time_from', 'end_time_to'):
        if vm_params.get(time_param):
            vm_params[time_param] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(int(vm_params.get(time_param)) / 1000))
    if not self.user.is_master_user:
        user_app_ids = self.auth_operation.get_user_vdc()
        vm_params['app_list_ids'] = user_app_ids
        vm_params['vm_customer_group'] = self.auth_operation.get_user_vm_custom_group()
    vms = list(cloud_models.VM.objects.filter_vm_list(vm_params))
    vm_dicts = self.vm_list_to_dict(vms)
    sort = vm_params.get('sort', 'create_time')
    if sort in ('pub_ip',):
        self.get_vm_card_info(vm_dicts)
    else:
        card_info_search_param = ['pub_ip', 'pri_ip', 'keyword', 'pub_flag', 'pri_flag', 'pub_name']
        for sp in card_info_search_param:
            if vm_params.get(sp):
                # 如果有上述任何一个查询条件，都会触发查询云主机的网卡
                self.get_vm_card_info(vm_dicts)
                break

    def ip_filter_vm(ip_addr, pipe_type=None):
        def _ip_filter_vm(_vm):
            if not ip_addr:
                return True
            # if hasattr(_vm, 'card_info'):
            if _vm.get('card_info'):
                for _c in _vm.get('card_info'):
                    if pipe_type:
                        if _c.get('pipe_type') == pipe_type and ip_addr in _c.get('ip'):
                            return True
                    elif ip_addr in _c.get('ip'):
                        return True
            return False

        return _ip_filter_vm

    def ip_filter_vm_by_flag(ip_addr, pipe_type=None):
        def _ip_filter_vm(_vm):
            if not ip_addr:
                return True
            # if hasattr(_vm, 'card_info'):
            if _vm.get('card_info'):
                for _c in _vm.get('card_info'):
                    if pipe_type:
                        if _c.get('pipe_type') == pipe_type and ip_addr == _c.get('ip'):
                            return True
                    elif ip_addr == _c.get('ip'):
                        return True
            return False

        return _ip_filter_vm

    def ip_name_filter_vm(pipe_name, pipe_type=None):
        def _ip_name_filter_vm(_vm):
            if not pipe_name:
                return True
            if _vm.get("card_info"):
                for _c in _vm.get("card_info"):
                    if pipe_type:
                        if _c.get("pipe_type") == pipe_type and pipe_name in _c.get("pipe_name"):
                            return True
                    elif pipe_name in _c.get("pipe_name"):
                        return True
            return False

        return _ip_name_filter_vm

    def ip_name_filter_vm_flag(pipe_name, pipe_type=None):
        def _ip_name_filter_vm(_vm):
            if not pipe_name:
                return True
            if _vm.get("card_info"):
                for _c in _vm.get("card_info"):
                    if pipe_type:
                        if _c.get("pipe_type") == pipe_type and pipe_name == _c.get("pipe_name"):
                            return True
                        elif pipe_name == _c.get("pipe_name"):
                            return True
            return False

        return _ip_name_filter_vm

    # 公网名称查询
    if vm_params.get("pub_name_flag"):  # 精确查询
        if vm_params.get("pub_name"):
            vms = filter(ip_name_filter_vm_flag(vm_params.get("pub_name"), 'public'), vms)
    else:
        if vm_params.get("pub_name"):
            vms = filter(ip_name_filter_vm(vm_params.get("pub_name"), 'public'), vms)

    # 多IP搜索实现
    if vm_params.get('pub_ip_flag'):  # 精准搜索
        if vm_params.get('pub_ip'):
            new_vms = list()
            for pub_ip in vm_params.get('pub_ip'):
                vms_select = filter(ip_filter_vm_by_flag(pub_ip.strip(), 'public'), vms)
                new_vms.extend(vms_select)
            vms = new_vms
    else:  # 模糊搜索
        if vm_params.get('pub_ip'):
            new_vms = list()
            for pub_ip in vm_params.get('pub_ip'):
                vms_select = filter(ip_filter_vm(pub_ip.strip(), 'public'), vms)
                new_vms.extend(vms_select)
            vms = new_vms

    if vm_params.get('pri_ip_flag'):  # 精准搜索
        if vm_params.get('pri_ip'):
            new_vms = list()
            for pri_ip in vm_params.get('pri_ip'):
                vms_select = filter(ip_filter_vm_by_flag(pri_ip.strip(), 'private'), vms)
                new_vms.extend(vms_select)
            vms = new_vms
    else:  # 模糊搜索
        if vm_params.get('pri_ip'):
            new_vms = list()
            for pri_ip in vm_params.get('pri_ip'):
                vms_select = filter(ip_filter_vm(pri_ip.strip(), 'private'), vms)
                new_vms.extend(vms_select)
            vms = new_vms

    # bug 出现重复的筛选项
    if vm_params.get('pri_ip') or vm_params.get('pub_ip'):
        vms_tmp = []
        for x in vms:
            if x not in vms_tmp:
                vms_tmp.append(x)
        vms = vms_tmp

    if vm_params.get('keyword'):
        vm_ids = [v.get('id') for v in vms]
        keyword = vm_params.get('keyword')
        keyword_vms = cloud_models.VM.objects.filter(Q(id__in=vm_ids),
                                                     (Q(name__contains=keyword)
                                                      | Q(app__name__contains=keyword)
                                                      | Q(app__site__name__contains=keyword)
                                                      | Q(app__site__city__name__contains=keyword)
                                                      | Q(app__site__city__zone__region__name__contains=keyword)
                                                      | Q(id__contains=keyword))
                                                     ).values('id')
        keyword_vm_ids = [v.get('id') for v in keyword_vms]
        # vms = filter(lambda x: x.id in keyword_vm_ids, vms)
        tmp_vms = filter(lambda x: x.get('id') in keyword_vm_ids, vms)
        tmp_vms = self.vm_list_to_dict(tmp_vms)
        ip_keyword_vms = filter(ip_filter_vm(keyword), vms)
        ip_keyword_vms = self.vm_list_to_dict(ip_keyword_vms)
        tmp_vms.update(ip_keyword_vms)
        vms = tmp_vms.values()

    vm_dicts = self.vm_list_to_dict(vms)
    if sort in ('end_time', '-end_time'):
        self.get_vm_bill_info(vm_dicts)
    else:
        bill_info_search_param = ['end_bill_time_from', 'end_bill_time_to', 'bill_method', 'bill_flag']
        for bs in bill_info_search_param:
            if vm_params.get(bs):
                self.get_vm_bill_info(vm_dicts)
                break

    def bill_end_time_filter_vm(time_str, op='ge'):
        """
        op: ge | gt | le | lt
        """
        o_time = strToDateTime(time_str)

        def _bill_end_time_filter_vm(_vm):
            # if hasattr(_vm, 'bill_info'):
            if _vm.get('bill_info'):
                vm_end_bill_time = _vm.get('bill_info').get('end_bill_time')
                if op == 'ge':
                    if vm_end_bill_time >= o_time:
                        return True
                    return False
                elif op == 'gt':
                    if vm_end_bill_time > o_time:
                        return True
                    return False
                elif op == 'le':
                    if vm_end_bill_time <= o_time:
                        return True
                    return False
                elif op == 'lt':
                    if vm_end_bill_time < o_time:
                        return True
                    return False
            if op in ('ge', 'gt'):
                # 按需默认终止时间2099-01-01，全部大于给定时间
                return True
            return False

        return _bill_end_time_filter_vm

    if vm_params.get('bill_method'):
        vms = filter(lambda x: x.get('bill_info', {}).get('bill_method', '0') == vm_params.get('bill_method'), vms)

    if vm_params.get('bill_method') != '0':
        if vm_params.get('end_time_from'):
            vms = filter(bill_end_time_filter_vm(vm_params.get('end_time_from'), 'ge'), vms)
        if vm_params.get('end_time_to'):
            vms = filter(bill_end_time_filter_vm(vm_params.get('end_time_to'), 'le'), vms)
    data = []
    suborder_end_time = datetime.datetime(year=2099, month=1, day=1)

    if sort == 'create_time':
        vms.sort(key=lambda _v: _v.get('create_time'))
    elif sort == '-create_time':
        vms.sort(key=lambda _v: _v.get('create_time'), reverse=True)
    elif sort == 'vm_name':
        vms.sort(key=lambda _v: _v.get('name'))
    elif sort == '-vm_name':
        vms.sort(key=lambda _v: _v.get('name'), reverse=True)
    elif sort == 'vm_rule':
        vms.sort(key=lambda _v: (_v.get('cpu'), _v.get('ram')))
    elif sort == '-vm_rule':
        vms.sort(key=lambda _v: (_v.get('cpu'), _v.get('ram')), reverse=True)
    elif sort == 'end_time':
        vms.sort(key=lambda _v: _v['bill_info'].get('end_bill_time', suborder_end_time) if _v.get(
            'bill_info') else suborder_end_time)
    elif sort == '-end_time':
        vms.sort(key=lambda _v: _v['bill_info'].get('end_bill_time', suborder_end_time) if _v.get(
            'bill_info') else suborder_end_time, reverse=True)
    elif sort == 'pub_ip':
        def sort_pub_ip_key(_vm):
            vm_cards = _vm.get('card_info', [])
            for _c in vm_cards:
                if _c.get('pipe_type') == 'public':
                    return _c.get('ip')
            return ''

        vms.sort(key=sort_pub_ip_key)
    if vm_params['page_flag']:
        total = len(vms)
        paginator = Paginator(vms, vm_params['page_size'])
        if vm_params['page_index'] <= (total / vm_params['page_size'] + 1):
            vms = list(paginator.page(vm_params['page_index']))
        else:
            vms = list()

    for vm in vms:
        # vm_status_str = vm_status_dict.get(vm.get("status"), _(u'未知'))
        if vm.get("status") == 'creating':
            vm_status_str = "创建" + str(vm.get("processing", 0)) + "%"

        vm_info = {
            'vm_id': vm.get('id'),
            'disk_size': vm.get('disk_size'),
            'vm_name': vm.get('name'),
            'vm_status': vm.get('status'),
            'service_status': vm.get('tools_status'),
            # 'service_status_str': tools_status_dict.get(vm.get("tools_status")),
            # 'vm_status_str': vm_status_str,
            'vspc_ip': vm.get('vspc_ip'),
            'vspc_port': vm.get("vspc_port"),
            'vc_name': vm.get("vc_name"),
            'create_time': vm.get('create_time').strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': vm.get('update_time').strftime('%Y-%m-%d %H:%M:%S'),
            'os_id': vm.get('os_id'),
            'os_name': vm.get('os__display_name'),
            'os_type': vm.get('os__os_type'),
            'os_version': vm.get('os__os_version'),
            'cpu_type': vm.get('cpu_type'),
            'os_template_type': vm.get('os__template_type'),
            'cpu': vm.get('cpu'),
            'ram': vm.get('ram'),
            'goods_id': vm.get('goods_id'),
            'conf_id': vm.get('goods__product_conf_id'),
            'app_id': vm.get('app_id'),
            'app_type': vm.get('app__type'),
            'app_name': vm.get('app__name'),
            'site_id': vm.get('app__site_id'),
            'site_name': vm.get('app__site__name'),
            'site_number': vm.get('app__site__number') or '',
            'city_name': vm.get('app__site__city__name'),
            'region_name': vm.get('app__site__city__zone__region__name'),
            'tags': ['asd', 'sdfe'],
            'type': vm.get('vm_type'),
            'is_nat': 1 if vm.get("goods__type") == 'nat' else 0,
            'product_id': vm.get("product_id") or '',
            'vm_bill_info' : {}
        }
        if settings.LANGUAGE_CODE == 'en':
            vm_info['city_name'] = vm.get('app__site__city__name_en')
            vm_info['region_name'] = vm.get('app__site__city__zone__region__name_en')
        data.append(vm_info)
    total = len(vms)
    # res_data = {'total': len(data), 'list': data}
    if vm_params['page_flag']:
        res_data = {'total': total, 'list': data}
        return CommonReturn(CodeMsg.SUCCESS, 'success', res_data)
    return CommonReturn(CodeMsg.SUCCESS, 'success', data)
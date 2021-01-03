def get_pub_info_by_vm_ids(self,vm_params):
    pub_pipe_obj_dict = {}
    vm_use_dict = {}
    pub_pipe_id_list = []
    pri_pipe_id_list = []
    segment_id_list = []
    pub_ip_list = []
    ddos_segments = []
    ddos_segment_ips = []
    for vm in vm_params:
        for c in vm.get('card_info', []):
            if c.get('pipe_type') == 'public':
                pub_pipe_id_list.append(c.get('pipe_id'))
                if c.get('segment_id'):
                    segment_id_list.append(c.get('segment_id'))
                    pub_ip_list.append(c.get('ip'))
    if vm_params.get('pub_flag'):
        if vm_params.get('pub_desc_flag'):
            pub_pipes = cloud_models.PipePublic.objects.filter(id__in=pub_pipe_id_list)
            map(lambda x: pub_pipe_obj_dict.update({x.id: x}), pub_pipes)
            vm_use = cloud_models.VMNetworkCard.objects.filter(pipe_id__in=pub_pipe_id_list,
                                                               connect=1,
                                                               vm__is_valid=1).values('pipe_id').annotate(
                vm_use_count=Count('pipe_id'))
            map(lambda x: vm_use_dict.update({x.get('pipe_id'): x.get('vm_use_count')}), vm_use)

        ddos_segments = cloud_models.DDOSSegment.objects.filter(pipe_public_segment_id__in=segment_id_list,
                                                                is_valid=1).values("pipe_public_segment_id", "id")
        ddos_segments = list(ddos_segments)
        ddos_segment_ips = cloud_models.DDOSSegmentIP.objects.filter(pub_ip__in=pub_ip_list,
                                                                     ros_nic__ros__customer_id=self.customer_id,
                                                                     type='ip',
                                                                     status=1).values("pub_ip", "address",
                                                                                      "ddos_segment_id")
        ddos_segment_ips = list(ddos_segment_ips)
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
        if vm_params.get('pub_flag'):
            # cards = vm.card_info if hasattr(vm, 'card_info') else []
            cards = vm.get('card_info', [])
            pub_info = []
            if vm.get('app__type') == 'VPC':
                eip_pub_obj = cloud_models.Eip.objects.filter(Q(resource_id=vm['id']) & Q(resource_type='VM') &
                                                              Q(is_valid=1)).first()
                if eip_pub_obj:
                    eip_pub_dict = {
                        'id': eip_pub_obj.id,
                        'ip': eip_pub_obj.ip,
                        'desc': eip_pub_obj.desc,
                        'base_qos': eip_pub_obj.qos,
                        'qos': eip_pub_obj.qos,
                        'status': eip_pub_obj.status,
                        'charge_type': EIP_CHARGE_TYPE.get(eip_pub_obj.charge_type),
                        'bandwidth_type': eip_pub_obj.bandwidth_type,
                        'resource_type': eip_pub_obj.resource_type,
                        "resource_id": eip_pub_obj.resource_id,
                    }
                    pub_info.append(eip_pub_dict)
                vm_info['pub_info'] = pub_info if pub_info else []
            else:
                for c in cards:
                    if c.get('pipe_type') == 'public':
                        pub_dict = {
                            'card_id': c.get('card_id'),
                            'ip': c.get('ip'),
                            'pipe_id': c.get('pipe_id'),
                            'mac': c.get('mac'),
                            'ipv6_bind': c.get('ipv6_bind', 0),
                            'ipv6_address': c.get('ipv6_address', ''),
                            'connected': c.get('connect'),
                            'segment_id': c.get('segment_id') or '',
                            "pipe_name": c.get("pipe_name", ''),
                            "pipe_type": c.get("pipe__pipe_type")
                        }
                        if vm_params.get('pub_desc_flag'):
                            pub_pipe = pub_pipe_obj_dict.get(c.get('pipe_id'))
                            wan_resource_suborder = WanResourceSuborder(pub_pipe)
                            # wan_bill_type = wan_resource_suborder.bill_type
                            wan_bill_type = pub_pipe.bill_type
                            wan_type_name = _(u'固定带宽')
                            wan_desc = ''
                            if wan_bill_type == 'number':
                                wan_desc = _(u'固定带宽') + '  %sMbps' % pub_pipe.qos
                            elif wan_bill_type == 'amount':
                                wan_type_name = _(u'流量包')
                                wan_desc = _(u'流量包') + '  %sGBps' % wan_resource_suborder.qos
                            elif wan_bill_type == 'peak':
                                wan_type_name = _(u'95峰值')
                                wan_desc = _(u'95峰值') + u'  保底：%sMbps' % wan_resource_suborder.qos
                            elif wan_bill_type == 'flow':
                                wan_type_name = _(u'流量')
                                wan_desc = _(u'流量') + '  %sMbps' % wan_resource_suborder.qos
                            elif wan_bill_type == 'flow_demand':
                                wan_type_name = _(u'流量按需')
                                wan_desc = _(u'流量按需') + '  %sMbps' % wan_resource_suborder.qos
                            conf_id = wan_resource_suborder.suborder.goods.product_conf_id
                            conf_name = wan_resource_suborder.suborder.goods.product_conf.name
                            pub_dict['pub_desc'] = {
                                'wan_type': wan_bill_type,
                                'wan_type_name': wan_type_name,
                                'wan_desc': wan_desc,
                                'goods_id': wan_resource_suborder.suborder.goods_id,
                                'conf_id': conf_id,
                                'conf_name': conf_name,
                                'qos': wan_resource_suborder.qos
                            }
                            pub_dict['pub_desc']['ipv6_display'] = int(bool(pub_pipe.ipv6_enable))
                            vm_use_count = vm_use_dict.get(c.get('pipe_id'), 0)
                            pub_dict['pub_desc']['vm_count'] = vm_use_count

                        # ddos ip 判断
                        if c.get('segment_id'):
                            pub_ip = c.get('ip')
                            segment_id = c.get('segment_id')
                            ip_info = self.new_get_vm_ip_info(segment_id=segment_id, pub_ip=pub_ip,
                                                              ddos_segments=ddos_segments,
                                                              ddos_segment_ips=ddos_segment_ips)
                            pub_dict["ddos_ip"] = ip_info.get("ddos_ip")
                            pub_dict["ddos_segment_id"] = ip_info.get("ddos_segment_id")
                            pub_dict["pub_ip"] = ip_info.get("pub_ip")

                        # 共享ddos判断
                        if not pub_dict.get("ddos_ip"):
                            ddos_ip = cloud_models.PipeIP.objects.filter(
                                vm_id=vm.get('id'), ddos_id__isnull=False,
                                status=1, address=c.get('ip')).first()
                            if ddos_ip:
                                pub_dict["ddos_ip"] = ddos_ip.address
                                pub_dict['pub_ip'] = ""
                        pub_info.append(pub_dict)
                vm_info['pub_info'] = pub_info
        data.append(vm_info)
    total = len(vms)
    # res_data = {'total': len(data), 'list': data}
    if vm_params['page_flag']:
        res_data = {'total': total, 'list': data}
        return CommonReturn(CodeMsg.SUCCESS, 'success', res_data)
    return CommonReturn(CodeMsg.SUCCESS, 'success', data)


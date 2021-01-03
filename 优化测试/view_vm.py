class VMViewSet(viewsets.GenericViewSet):
    @list_route(methods=['POST'], url_path='search', serializer_class=vm_serializers.VMSearchSerializer)
    @api_serializer_deco(u'搜索云主机')
    def search(self, request, serializer_data=None):
        data = serializer_data
        vm_resource = VMResource(customer=request.user.customer,
                                 user=request.user)
        return vm_resource.search_vm_list(data)

    @list_route(methods=['POST'], url_path='os_and_disk_info', serializer_class=vm_serializers.VMSearchSerializer)
    @api_serializer_deco(u'获取操作系统和磁盘信息')
    def os_and_disk_info(self, request, serializer_data=None):
        data = serializer_data
        vm_resource = VMResource(customer=request.user.customer,
                                 user=request.user)
        return vm_resource.get_os_and_disk_info_by_vm_ids(data)

    @list_route(methods=['POST'], url_path='vm_bill_info', serializer_class=vm_serializers.VMSearchSerializer)
    @api_serializer_deco(u'获取云主机计费信息')
    def vm_bill_info(self, request, serializer_data=None):
        data = serializer_data
        vm_resource = VMResource(customer=request.user.customer,
                                 user=request.user)
        return vm_resource.get_vm_bill_by_vm_ids(data)

    @list_route(methods=['POST'], url_path='pub_info', serializer_class=vm_serializers.VMSearchSerializer)
    @api_serializer_deco(u'获取公网信息')
    def pub_info(self, request, serializer_data=None):
        data = serializer_data
        vm_resource = VMResource(customer=request.user.customer,
                                 user=request.user)
        return vm_resource.get_pub_info_by_vm_ids(data)

    @list_route(methods=['POST'], url_path='private_info', serializer_class=vm_serializers.VMSearchSerializer)
    @api_serializer_deco(u'获取私网信息')
    def private_info(self, request, serializer_data=None):
        data = serializer_data
        vm_resource = VMResource(customer=request.user.customer,
                                 user=request.user)
        return vm_resource.get_private_info_by_vm_ids(data)

    @list_route(methods=['POST'], url_path='dedicated_info', serializer_class=vm_serializers.VMSearchSerializer)
    @api_serializer_deco(u'获取专属云信息')
    def dedicated_info(self, request, serializer_data=None):
        data = serializer_data
        vm_resource = VMResource(customer=request.user.customer,
                                 user=request.user)
        return vm_resource.get_dedicated_info_by_vm_ids(data)

    @list_route(methods=['POST'], url_path='nic_left_info', serializer_class=vm_serializers.VMSearchSerializer)
    @api_serializer_deco(u'获取缺失网卡的数量')
    def nic_left_num(self, request, serializer_data=None):
        data = serializer_data
        vm_resource = VMResource(customer=request.user.customer,
                                 user=request.user)
        return vm_resource.get_dnic_left_num_info_by_vm_ids(data)

    @list_route(methods=['POST'], url_path='conf_info', serializer_class=vm_serializers.VMSearchSerializer)
    @api_serializer_deco(u'获取产品配置信息')
    def conf_info(self, request, serializer_data=None):
        data = serializer_data
        vm_resource = VMResource(customer=request.user.customer,
                                 user=request.user)
        return vm_resource.get_conf_info_by_vm_ids(data)






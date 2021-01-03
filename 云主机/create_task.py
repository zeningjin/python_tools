# @classmethod
    # def create_task(cls, operation: ResUserOperation):
    #     type = 'operation'
    #     try:
    #         # count = 0
    #         # self.close_old_connections()
    #
    #         with transaction.atomic():
    #             if operation.task_id or operation.task_status:
    #                 raise Exception(u'op has operate')
    #             operation.task_status = 'LOCK'
    #
    #             parameter = operation.detail
    #             data = json.loads(parameter)
    #             task_type = data.get('task_type')
    #
    #             # data中更新operation_id,
    #             data.update({
    #                 'operation_id': operation.id
    #             })
    #
    #
    #             out_param = json.dumps(sub_create_vm)
    #             task_type = out_param.get('task_type') if out_param.get(
    #                 'task_type') else task_type
    #             cloud_id = get_cloud_id(out_param)
    #             if cloud_id is None:
    #                 d = "empty"
    #             else:
    #                 d = cloud_id
    #
    #             logger.info("***********task_type:" + task_type)
    #             logger.info("***********cloud_id:" + d)
    #             logger.info("***********params:" + str(out_param))
    #
    #             staff_id = operate.agent_user_id
    #             app_id = out_param.get('app_id') if out_param.get(
    #                 'app_id') else out_param.get('appId')
    #             area_id = out_param.get('area_id', "CN")
    #             customer_user_id = operate.customer_user_id
    #             customer_id = operate.customer_user.customer_id
    #             out_param.update({'customer_id': customer_id})
    #             task_version = TASK_TYPE_VERSION.TASK_VERSION(customer_user_id)
    #             source_type = type
    #             source_id = operation_id
    #             logger.info('operation_id = [%s] parameter=[%s]' % (
    #                 operation_id, parameter))
    #             task = save_task(task_type, app_id, area_id, customer_id, json.dumps(out_param), task_version, cloud_id,
    #                              customer_user_id,
    #                              staff_id,
    #                              source_type, source_id)
    #             operate.task_id = task.id
    #             operate.save()
    #             return task

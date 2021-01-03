# -*- coding: utf-8 -*-
# @Time    : 2021/1/3 下午7:40
# @Author  : jinzening
# @File    : OverView.py
# @Software: PyCharm
from pyVim import connect
from pyVmomi import vim


def print_vm_info(virtual_machine):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    summary = virtual_machine.summary
    print("Name       : ", summary.config.name)
    print("Template   : ", summary.config.template)
    print("Path       : ", summary.config.vmPathName)
    print("Guest      : ", summary.config.guestFullName)
    print("Instance UUID : ", summary.config.instanceUuid)
    print("Bios UUID     : ", summary.config.uuid)
    print("State      : ", summary.runtime.powerState)

    # 判断是否有注释
    annotation = summary.config.annotation
    if annotation:
        print("Annotation : ", annotation)

    # 打印Guest OS内的信息
    if summary.guest is not None:
        ip_address = summary.guest.ipAddress
        tools_version = summary.guest.toolsStatus
        if tools_version is not None:
            print("VM-tools: ", tools_version)
        else:
            print("V-tools: None")
        if ip_address:
            print("IP         : ", ip_address)
        else:
            print("IP         : None")


def print_vm_runtime(virtual_machine):
    """
    虚拟机状态、配置信息
    :param virtual_machine:
    :return:
    """
    # runtime = (vim.vm.RuntimeInfo) {
    #       dynamicType = <unset>,
    #       host = 'vim.HostSystem:host-34',
    #       connectionState = 'connected',
    #       powerState = 'poweredOn',　　// 虚拟机电源状态
    #       faultToleranceState = 'notConfigured',　　// 是否配置FT
    #       dasVmProtection = <unset>,
    #       toolsInstallerMounted = false,
    #       suspendTime = <unset>,
    #       bootTime = 2017-08-26T06:31:27.543474Z,
    #       suspendInterval = 0,
    #       question = <unset>,
    #       memoryOverhead = <unset>,
    #       maxCpuUsage = 2808,
    #       maxMemoryUsage = 891,
    #       numMksConnections = 0,
    #       recordReplayState = 'inactive',
    #       cleanPowerOff = <unset>,
    #       needSecondaryReason = <unset>,
    #       onlineStandby = false,
    #       minRequiredEVCModeKey = <unset>,
    #       consolidationNeeded = false,
    # }
    runtime = virtual_machine.runtime
    print("dynamicType       : ", runtime.dynamicType)
    print("host       : ", runtime.host)
    print("connectionState       : ", runtime.connectionState)
    print("powerState       : ", runtime.powerState)
    print("faultToleranceState       : ", runtime.faultToleranceState)
    print("dasVmProtection       : ", runtime.dasVmProtection)
    print("toolsInstallerMounted       : ", runtime.toolsInstallerMounted)
    print("bootTime       : ", runtime.bootTime)
    print("maxCpuUsage       : ", runtime.maxCpuUsage)


def print_vm_guest(virtual_machine):
    """
    Guest操作系统信息
    :param virtual_machine:
    :return:
    """
    # guest = (vim.vm.Summary.GuestSummary) {
    #       dynamicType = <unset>,
    #       dynamicProperty = (vmodl.DynamicProperty) [],
    #       guestId = 'ubuntu64Guest',
    #       guestFullName = 'Ubuntu Linux (64-bit)',
    #       toolsStatus = 'toolsOk',　　// VMtools状态
    #       toolsVersionStatus = 'guestToolsUnmanaged',
    #       toolsVersionStatus2 = 'guestToolsUnmanaged',
    #       toolsRunningStatus = 'guestToolsRunning',
    #       hostName = 'ubuntu001',　　// hostname
    #       ipAddress = '172.16.65.146'　　// ipaddress
    # }
    guest = virtual_machine.summary.guest
    print("guestId       : ", guest.guestId)


def print_vm_config(virtual_machine):
    """
    虚拟机配置
    :param virtual_machine:
    :return:
    """
    # config = (vim.vm.Summary.ConfigSummary) {
    #       dynamicType = <unset>,
    #       dynamicProperty = (vmodl.DynamicProperty) [],
    #       name = 'Ubuntu16.04',
    #       template = false,
    #       vmPathName = '[datastore1] Ubuntu16.04/Ubuntu16.04.vmx',
    #       memorySizeMB = 1024,
    #       cpuReservation = 0,
    #       memoryReservation = 0,
    #       numCpu = 1,
    #       numEthernetCards = 1,
    #       numVirtualDisks = 1,
    #       uuid = '4239b0ea-cbb8-c0b2-56a1-0b98bdbf01dd',
    #       instanceUuid = '5039f07c-47c6-d77d-e793-bf1b7aee17e2',
    #       guestId = 'ubuntu64Guest',
    #       guestFullName = 'Ubuntu Linux (64-bit)',
    #       annotation = 'Ubuntu Server',
    #       product = <unset>,
    #       installBootRequired = false,
    #       ftInfo = <unset>,
    #       managedBy = <unset>
    #    }
    config = virtual_machine.summary.config
    print("name       : ", config.name)
    print("numCpu       : ", config.numCpu)


def print_vm_storage(virtual_machine):
    """
    虚拟机磁盘信息
    :param virtual_machine:
    :return:
    """
    # storage = (vim.vm.Summary.StorageSummary) {
    #       dynamicType = <unset>,
    #       dynamicProperty = (vmodl.DynamicProperty) [],
    #       committed = 18424777995,
    #       uncommitted = 505,
    #       unshared = 17179869184,
    #       timestamp = 2017-08-26T08:37:37.764585Z
    #    }
    storage = virtual_machine.summary.storage
    print("committed       : ", storage.committed)
    print("uncommitted       : ", storage.uncommitted)


def get_connect():
    vc_host = '10.128.232.101'
    vc_user = 'administrator@vsphere.local'
    vc_ds= 'ma-ds-5277578c-be886277-1ac9-3086db8d4ac5'
    vc_password = 'VMware1!'
    service_instance = connect.SmartConnectNoSSL(host=vc_host,
                                                 user=vc_user,
                                                 pwd=vc_password,
                                                 port=443
                                                 )
    return service_instance


if __name__ == '__main__':

    service_instance = get_connect()
    content = service_instance.RetrieveContent()  # 拿到vCenter的内容对象
    container = content.rootFolder  # starting point to look into
    view_type = [vim.VirtualMachine]  # object types to look for
    recursive = True  # whether we should look into it recursively
    container_view = content.viewManager.CreateContainerView(container, view_type, recursive)

    children = container_view.view
    for child in children:
        print_vm_info(child)
        print_vm_runtime(child)
        print_vm_guest(child)
        print_vm_config(child)
        print_vm_storage(child)

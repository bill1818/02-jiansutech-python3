#!/usr/bin/env python3
#create at 2018-11-30
'this is a system monitor scripts'
__author__="yjt"
 
import os
import time
import sys
import datetime
import socket  #用于获取主机名
import psutil  #用于获取CPU等信息（该模块属于第三方模块，需要安装；或者安装anaconda3，anaconda3默认已经安装好改模块）
import re
 
#以下是变量值，自己定义
CPUT = 2      #计算CPU利用率的时间间隔
NETT = 2      #计算网卡流量的时间间隔
LOOPT = 2     #脚本循环时间间隔
 
#获取系统基本信息
def baseinfo():
    hostname = socket.gethostname()
    start_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#    sys_runtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() - psutil.boot_time()))
    sys_runtime = os.popen('w').readline().split('users')[0].split('up')[1].strip()[:-1].strip()[:-1]
    print("\033[31mbase_info:\033[0m")
    print("hostname:    %-10s"%(hostname))
    print("start_time:  %-15s"%(start_time))
    print("now_time:    %-15s"%(now_time))
    print("sys_runtime: %-10s"%(sys_runtime))
def userconninfo():
    print("\033[31muser_conn_info:\033[0m")
    user_conn = len(psutil.users())
    print("user_conn_num:%s"%(user_conn))
    print("conn_user%-10s conn_terminal%-10s remmote_ip%-10s start_time%-15s pid%-15s"%('','','','',''))
    for info in range(user_conn):
        user = psutil.users()[info].name
        terminal = psutil.users()[info].terminal
        host = psutil.users()[info].host
        start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(psutil.users()[0].started))
        pid = psutil.users()[info].pid
        #print("conn_user:%-10s conn_terminal:%-10s from_host:%-15s start_time:%-20s pid:%-10d"%(user,terminal,host,start_time,pid))
        print("%-19s %-23s %-20s %-25s %-15d"%(user,terminal,host,start_time,pid))
#获取CPU信息
def cpuinfo():
    ave_load = os.popen('uptime').readline().split(":")[-1].split()
    ave_load = ' '.join(ave_load) #CPU平均负载
    #以下四项值都是获取的瞬时值
    user_use = psutil.cpu_times().user  #用户态使用CPU时间
    sys_use = psutil.cpu_times().system #系统态使用CPU时间
    idle = psutil.cpu_times().idle #CPU空闲时间
    iowait = psutil.cpu_times().iowait #IO等待时间
    total_cpu = 0
    for i in range(len(psutil.cpu_times())):
        total_cpu += psutil.cpu_times()[i] 
    cpu_pre = psutil.cpu_percent(CPUT)
    logical_cpu = psutil.cpu_count()
    pyhsical_cpu = psutil.cpu_count(logical=False)
    print("\033[31mcpu_info:\033[0m")
    print("cpu_ave_load:    %-20s" %ave_load)
    print("cpu_user_use:    %-.2f%%" %(user_use / total_cpu * 100))
    print("cpu_sys_use:     %-.2f%%" %(sys_use  / total_cpu * 100))
    print("cpu_idle:        %-.2f%%" %(idle / total_cpu * 100 ))
    print("cpu_iowait:      %-.2f%%" %(iowait / total_cpu * 100 ))
    print("cpu_ave_use:     %-.2f%%" %cpu_pre)
    print("logica_cpu:      %-4d"%logical_cpu) #获取逻辑CPU个数
    print("pyhsical_cpu:    %-4d"%pyhsical_cpu)#获取物理CPU个数
#获取内存信息
def meminfo():
    total_mem = psutil.virtual_memory().total
    use_mem = psutil.virtual_memory().used
    mem_percent = psutil.virtual_memory().percent
    free_mem = psutil.virtual_memory().free
    swap_mem = psutil.swap_memory().total
    swap_use = psutil.swap_memory().used
    swap_free = psutil.swap_memory().free
    swap_percent = psutil.swap_memory().percent
    print("\033[31mmem_info:\033[0m")
    print("total_mem:     %d M"%(total_mem / 1024 /1024))
    print("use_mem:       %d M"%(use_mem / 1024 /1024))
    print("free_mem:      %d M"%(free_mem / 1024 /1024))
    print("mem_percent:   %s%%"%(mem_percent))
    print("swap_mem:      %d M"%(swap_mem / 1024 /1024))
    print("swap_use:      %d M"%(swap_use / 1024 /1024))
    print("swap_free:     %d M"%(swap_free / 1024 /1024))
    print("swap_percent:  %s%%"%(swap_percent))
#获取磁盘信息
def diskinfo():
    print("\033[31mdisk_info:\033[0m")
    print("disk%-10s total%-10s free%-10s used%-10s percent%-10s"%('','(G)','(G)','(G)','(%)'))
    disk_len = len(psutil.disk_partitions())
    for info in range(disk_len):
        disk = psutil.disk_partitions()[info][1]
        if len(disk) < 10:
            total = str(round(psutil.disk_usage(disk).total /1024/1024/1024)) + 'G'
            free = str(round(psutil.disk_usage(disk).free /1024/1024/1024)) + 'G'
            used = str(round(psutil.disk_usage(disk).used /1024/1024/1024)) + 'G'
            percent = str(psutil.disk_usage(disk).percent) + '%'
            print('%-15s'%(disk),end='')
            #print(' %-10s  total: %-10s  free: %-10s  used:%-10s  percent:%-s'%('',total,free,used,percent))
            print('%-13s   %-13s  %-13s  %-s'%(total,free,used,percent))
#获取网卡信息
def netinfo():
    print('\033[31mnet_info\033[0m')
    net_item = list(psutil.net_if_addrs())
    for net in net_item:
        if re.search(r'bond.*|em.*|eno.*|^eth.*',net):
            network_card = net
            ip = psutil.net_if_addrs()[net][0].address
            recv_1,recv_2,send_1,send_2=0,0,0,0
            with open ('/proc/net/dev','r') as f:
                net_info = f.readlines()
                net_list = str(net_info).lower().split()
                if net_list[0] == net:
                    recv_1 = float(net_list[1])
                    send_1 = float(net_list[9])
            time.sleep(NETT)
            with open ('/proc/net/dev','r') as f:
                net_info = f.readlines()
                net_list = str(net_info).lower().split()
                if net_list[0] == net:
                    recv_2 = float(net_list[1])
                    send_2 = float(net_list[9])
            print("network_card%-10s  ip%-20s received%-10s  transmit%-10s "%('','','(kb/s)','(kb/s)'))
            #print("network_card: %-10s  ip: %-20s received: %-.3f Kb/s transmit: %-.3f kb/s" % (network_card,ip,(recv_2/1024 - recv_1/1024),(send_2/1024 - send_1/1024)))
            print("%-21s   %-22s %-.3f%13s  %-.3f " % (network_card,ip,(recv_2/1024 - recv_1/1024),'',(send_2/1024 - send_1/1024)))
#获取TCP连接数
def tcpinfo():
    print('\033[31mtcp_info\033[0m')
    status_list = ["LISTEN","ESTABLISHED","TIME_WAIT","CLOSE_WAIT","LAST_ACK","SYN_SENT"]
    status_init = []
    net_conn =  psutil.net_connections()
    for key in net_conn:
        status_init.append(key.status)
    for value in status_list:
        print(value,status_init.count(value))
 
 
if __name__ == '__main__':
    while True:
        try:
            os.system('clear')
            baseinfo()
            print("********************************************************")
            userconninfo()
            print("########################################################")
            cpuinfo()
            print("========================================================")
            meminfo()
            print("########################################################")
            diskinfo()
            print("********************************************************")
            netinfo()
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            tcpinfo()
            time.sleep(LOOPT)
        except KeyboardInterrupt as e:
            print ('')
            print("Bye-Bye")
            sys.exit(0)
# -*- coding: utf-8 -*-
# @Time : 2020-4-10 22:13
# @Author : yejunhai
# @Site :
# @File : port_monitor.py
# @Software: PyCharm


import pymysql
import socket
import sys
import time
import requests
import json


def msg(text) :
    #发送到企业微信机器人
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    api_url = ""  # 这个是企业微信机器人生成的webhook地址，修改为你的即可。
    json_text = {
        "msgtype" : "text",
        "text" : {
            "content" : text
        },
    }
    requests.post(api_url, json.dumps(json_text), headers=headers).content

def port_check(ip,port):
    #检查socket返回值
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(2)
    result=s.connect_ex((ip,int(port)))
    return result

def out_log(text):
    #运行写日志。。。。。。。
    with open(f'{sys.argv[0].split(".")[0]}.log','a') as f:
        print(text,file=f)


def down_time(ip):
    #计算故障时间，mysql自带也可以计算，不会- -！
    cursor.execute(f"SELECT mzt.start_time,mzt.end_time FROM mzt WHERE mzt.ip = '{ip}'")
    total_time = cursor.fetchone()
    try:
        start_time = total_time[0]
        end_time =total_time[1]
        duration = end_time-start_time
        return f"\n本次故障开始时间 {start_time}\n本次故障结束时间 {end_time}\n本次故障持续时间 {duration}"
    except:
        return "\n故障开始时间未记录"

#时间格式
cur_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

# 打开数据库连接
db = pymysql.connect("127.0.0.1",user = "root",passwd = "root",db = "zwy")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 查询语句
sql = "SELECT mzt.ip,mzt.port1,mzt.port2,mzt.send,mzt.`部署业务` FROM mzt "
# try:

cursor.execute(sql)
results = cursor.fetchall()
#获取到IP和端口开始搞事
for row in results:
    ip=row[0]
    port1=row[1]
    port2=row[2]
    send=row[3]
    description=row[4]
    #检查多个端口
    for port in port1,port2:
        if port != '' and port != None:
            port_status=port_check(ip,port)
            if port_status != 0 and send == 0:
                cursor.execute(f"UPDATE mzt SET send = '1' WHERE mzt.ip = '{ip}'") #发生告警后更新防止一直告警
                cursor.execute(f"UPDATE mzt SET start_time = '{cur_time}' WHERE mzt.ip = '{ip}'") #记录故障时间
                db.commit()
                msg(f"{cur_time} {description} {ip}:{port} 端口关闭，请检查!") #发送告警
                out_log(f"{cur_time} {ip}:{port} check {port_status} send: {send}") #写入日志
            elif port_status == 0 and send == 1:
                cursor.execute(f"UPDATE mzt SET send = '0' WHERE mzt.ip = '{ip}'")
                cursor.execute(f"UPDATE mzt SET end_time = '{cur_time}' WHERE mzt.ip = '{ip}'")
                db.commit()
                msg(f"{cur_time} {description} {ip}:{port} 端口恢复.{down_time(ip)}")
                out_log(f"{cur_time} {ip}:{port} check {port_status} send: {send}")
            else:
                out_log(f"{cur_time} {ip}:{port} check {port_status} send: {send}")
# except:
#     print("Error: unable to fetch data")
#关闭数据库
db.close()



#老传统crontab定时的跑就完事了

#    */1 * * * * /usr/bin/python3 /root/port_monitor.py

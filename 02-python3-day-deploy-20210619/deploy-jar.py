#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os, signal,sys,time


def kill_port(target):
    cmd_run = 'lsof -i tcp:{}'.format(target)
    os.system(cmd_run)
    out = os.popen(cmd_run).read()
    for line in out.splitlines():
        print(line)
        if 'IPv6' in line:
            pid = str(line.split()[1])  # 得到pid
            print('pid=' + pid)
            time.sleep(3)
            os.system('kill -9 %s' % pid)
            out = os.popen(cmd_run).read()
            if out!="":
                print('kill 完成')


def run_jar(jar_name):
    cmd_run = "nohup java -jar {}".format(jar_name)+" &"
    print(cmd_run)
    os.system(cmd_run)
    out = os.popen(cmd_run).read()
    if out!="":
        os.system("tail -200f nohup.out")


if __name__ == '__main__':
    kill_port(8888)
    run_jar("demo-0.0.1-SNAPSHOT.jar")

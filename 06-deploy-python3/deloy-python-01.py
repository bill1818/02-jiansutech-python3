#!/usr/bin/python env
# -*- coding: utf-8 -*-

import os, sys, paramiko, time

date = time.strftime("%Y%m%d%H%M%S", time.localtime)

class Connection(object):
    def __init__(self, ip, user, remote_file, port=22, key='/root/.ssh/id_rda'):
        self.ip = ip
        self.user = user
        self.port = int(port)
        self.remote_file = remote_file
        self.private_key = paramiko.R




dat
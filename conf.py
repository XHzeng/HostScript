#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:Zeng Xianhe
#host_list列表是除namenode1以外的所有机器ip,主机名
host_list = [
     ('192.168.0.183','node1'),
     ('192.168.0.190','node2'),
     ('192.168.0.200','node3'),
]


#ROOT用户执行的命令
ROOT = [
    'sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config',
    'setenforce 0',
    'groupadd soft && useradd -g soft soft && echo "soft@2016" |  passwd --stdin soft',           #用户名和组可以自己更改
    'sed -i "s/#   StrictHostKeyChecking ask/StrictHostKeyChecking no/g" /etc/ssh/ssh_config',
    'systemctl stop firewalld.service && systemctl disable firewalld.service',
]

#普通用户执行的命令
USER = [
    'ssh-keygen -t rsa -P  "" -f /home/soft/.ssh/id_rsa',
    'cat /home/soft/.ssh/id_rsa.pub > /home/soft/.ssh/authorized_keys',
    'chmod 600 /home/soft/.ssh/authorized_keys',
]

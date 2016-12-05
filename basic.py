#!/usr/bin/env python
#-*- coding:utf-8 -*-
import  paramiko
from conf import host_list,ROOT,USER


##更改hosts文件,配置主机解析
with open('hosts','a') as f1:
    for i in host_list:
        f1.write(i[0]+' '+i[1])
        f1.write('\n')

def change_hosts(host,user,passwd):
    '''
    #上传hosts文件到各个服务器
    :param host:     主机ip
    :param user:     主机用户名
    :param passwd:   用户名密码
    :return:
    '''
    transport = paramiko.Transport((host,22))
    transport.connect(username=user,password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    print host
    sftp.put('hosts','/etc/hosts')
    transport.close()


def root(host,hostname,user,pwd):
    '''
    :param host:        # 主机ip
    :param hostname:    # 主机名
    :param user:        # 主机用户名
    :param pwd:         # 用户名密码
    :return:            # 默认为none
    1. 更改主机名
    2. 关闭selinux和firewalld防火墙
    3. 创建用户和组并设置密码
    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host,username=user,password=pwd,port=22,)
    setname = 'echo' + ' ' + hostname + ' ' + '> /etc/hostname'        #更改主机名
    ROOT.append(setname)                                                    #将更改主机名命令添加到cmd列表中
    for item in ROOT:
        print(item)
        stdin, stdout, stderr = ssh.exec_command(item)
    ROOT.remove(setname)                                                   #将命令移除,防止下次循环多一条命令
    ssh.close()

def user(host,user,pwd,cmd):
    '''
    :param host:        # 主机ip
    :param user:        # 主机用户名
    :param pwd:         # 用户名密码
    :param cmd:         # 普通用户执行的命令
    :return:            # 默认为none
    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host,username=user,password=pwd,port=22,)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    ssh.close()

#下载所有机器的authorized_keys文件
def getfile(host,user,passwd):
    '''
    :param host:   主机ip
    :param user:   主机用户名
    :param passwd: 用户名密码
    :return:       默认为none
    从每台服务器上下载authorized_keys文件到当前目录,并以ip命名
    '''
    transport = paramiko.Transport((host,22))
    transport.connect(username=user,password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get('/home/soft/.ssh/authorized_keys', str(host))
    transport.close()

def putfile(host,user,passwd):
    '''
    :param host:     主机ip
    :param user:     主机用户名
    :param passwd:   用户名密码
    :return:         默认为none
    put authorized文件到每台服务器
    '''
    transport = paramiko.Transport((host,22))
    transport.connect(username=user,password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('authorized', '/home/soft/.ssh/authorized_keys')
    transport.close()

if __name__ == '__main__':
    while True:
        username = raw_input('输入你的用户名: ')
        passwd = raw_input('输入你的密码：')
        if username == 'root':
            for i in host_list:
                root(i[0],i[1],username,passwd)
                change_hosts(i[0],username,passwd)
        elif username == 'soft':
            for i in host_list:
                #执行普通用户的命令
                for shell in USER:
                    user(i[0],username,passwd,shell)                    
            #循环机器列表,从每台服务器上下载authorized_keys文件        
            for host in host_list:
                getfile(host[0],username,passwd)
        #循环每个机器的auth文件,然后把内容追加到authorized文件中
            for hosts in host_list:
                with open(str(hosts[0]),'r') as f1,open('authorized','a') as f2:
                    for i in f1.readlines():
                        f2.write(i.strip())
                        f2.write('\n')
            #循环机器列表,将authorized文件上传到每台服务器
            for ip in host_list:
                putfile(ip[0],username,passwd)
        else:
            exit()

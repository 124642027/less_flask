__author__ = 'liht'

# !/usr/bin/env python
# -*-coding:utf-8 -*-
# 确保用户登录的权限
# gateway设置跳板机

from fabric.api import *


env.user = 'web'


env.hosts = ['192.168.7.36:8070']

def pack():

    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    dist = local('python setup.py --fullname', capture=True).strip()

    put('dist/%s.tar.gz' % dist, '/tmp/yourapplication.tar.gz')

    run('mkdir /tmp/yourapplication')
    with cd('/tmp/yourapplication'):
        run('tar xzf /tmp/yourapplication.tar.gz')

        run('/var/www/yourapplication/env/bin/python setup.py install')

    run('rm -rf /tmp/yourapplication /tmp/yourapplication.tar.gz')

    run('touch /var/www/yourapplication.wsgi')

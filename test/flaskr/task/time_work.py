#-*- coding:utf-8 -*-
"""
使用celery实现两种形式的任务，
1.client-work模式任务，本文件提供work定义，执行time_job，传递执行work中的job信号，work收到后执行
使用命令celery -A time_work worker --loglevel=info启动work
2.实现crontab定时任务，使用config_from_object获取配置
使用命令celery -A time_work beat启动work；此时也要使用1中的命令，启动work；
每个周期执行work中的任务;任务的周期在conf中配置
"""
from celery import Celery
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)


c = Celery('time_work', broker='redis://192.168.6.184:6389/0')
c.config_from_object('conf.task_conf')

@c.task
def hello(x, y):
    return 'hello world', x * 20, y*20

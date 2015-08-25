#-*- coding:utf-8 -*-
# 执行python time_job，手动将job推到celery中执行
from time_work import hello
hello.delay(4, 5)
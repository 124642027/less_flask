#! /usr/bin/env python
#-*-coding:utf-8-*-
# configuration, SECRET_KEY是系统内置的属性，对应有一定的作用
# 由于app.config是个字典对象，我们可以新加属性到config里面;这里添加后，在app.config总就可以直接使用了
DATABASE = 'flaskr.db'
DEBUG = False
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# mail
ADMINS = ['mail@sina.com']

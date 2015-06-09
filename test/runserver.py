#!/usr/bin/env python
# -*-coding:utf-8-*-

# 启动应用
# 启动时自动加载flaskr文件夹中的__init__.py，启动相应的环境的配置，启动应用

from flaskr import app
import argparse

parser = argparse.ArgumentParser(description='run the app')
parser.add_argument('-e', '--env', type=str, help="choose environment", default="test")
args = parser.parse_args()

# app.config.from_object(__name__)
if args.env == "product":
    app.config.from_object('flaskr.conf.product')
else:
    app.config.from_object('flaskr.conf.test')

app.run(host="0.0.0.0", port=8683, debug=True)

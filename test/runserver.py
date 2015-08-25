#!/usr/bin/env python
# -*-coding:utf-8-*-

# 启动应用
# 启动时自动加载flaskr文件夹中的__init__.py，启动相应的环境的配置，启动应用

# app对象是的使用，在runserver启动的时候，引入对应文件夹的app；这时会执行文件夹中的__init__，生成相应的app
# 同时可以在文件夹的其他文件中，使用 from youapplication import app的形式引入app对象

# 启动flaskr应用
# from flaskr import app
# import argparse
#
# parser = argparse.ArgumentParser(description='run the app')
# parser.add_argument('-e', '--env', type=str, help="choose environment", default="test")
# args = parser.parse_args()
#
# # app.config.from_object(__name__)
# if args.env == "product":
#     app.config.from_object('flaskr.conf.product')
# else:
#     app.config.from_object('flaskr.conf.test')
#
# app.run(host="0.0.0.0", port=8683, debug=True)


# 启动hello_app应用

# from hello_app import app
# from werkzeug.serving import run_simple
# run_simple('localhost', 5000, app,
#             use_reloader=True, use_debugger=True, use_evalex=True)


# 同时启动多个应用
# from werkzeug.wsgi import DispatcherMiddleware
# from flaskr import app as flaskrend
# from hello_app import app as helloend
#
# application = DispatcherMiddleware(flaskrend, {"/backend": helloend})


# 新建flask-admin入口
from flask_manage import app
app.run(host="0.0.0.0", debug=False)
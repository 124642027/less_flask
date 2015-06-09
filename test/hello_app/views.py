# !/usr/bin/env python
# -*-coding:utf-8

from hello_app import app
from flask import jsonify, g, Blueprint
from define_exception import InvalidUsage

bp = Blueprint('frontend', __name__, url_prefix='lang_code')

# 将url中的lang_code参数传入方法中
@bp.route('/')
def hello_world():
    # raise InvalidUsage('This view is gone', status_code=410)
    return 'Hello World!'

# 使用自定义异常类之前，要注册这个异常类的视图入口(处理句柄);
# 使用自定义类必须实现异常处理句柄，因为调用过程是，触发异常，执行异常类的初始化方法；
# 然后进入异常处理句柄，格式化好返回的属性，然后触发自定义异常的部分才能获取结果
@bp.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# 使用url处理器统一 处理包含相同部分的url
@bp.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)
    # if 'lang_code' in values or not g.lang_code:
    #     return
    # if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
    #     values['lang_code'] = g.lang_code

@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code', None)
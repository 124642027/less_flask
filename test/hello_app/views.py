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

# 实现url的延迟加载
from werkzeug import import_string, cached_property


class LazyView(object):
    def __init__(self, import_name):
        print "*" * 30
        # add_url_rule如果没有传入endpoint的值，那么程序会回去view_fun指向的__name__
        # 所以这里面给__name__赋值
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name

    @cached_property
    def view(self):
        print "=" * 30
        return import_string(self.import_name)

    # __call__实现的是方法的调用时的动作，本处是view_func执行时的动作;
    def __call__(self, *args, **kwargs):
        print "&" * 30
        return self.view(*args, **kwargs)


# 在app启动的时候，只加载LazyView的__init__方法,只有在有http请求的时候，才调用view方法，
# 这样可以让view在有http请求的时候才加载
app.add_url_rule('/hello',
                 view_func=LazyView('hello_app.views.hello'))


def hello():
    return "hello"
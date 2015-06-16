# !/usr/bin/env python
# -*-coding:utf-8

from hello_app import app
from flask import jsonify, g, Blueprint, url_for
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
        # print "*" * 30
        # add_url_rule如果没有传入endpoint的值，那么程序会回去view_fun指向的__name__
        # 所以这里面给__name__赋值
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name

    @cached_property
    def view(self):
        # print "=" * 30
        return import_string(self.import_name)

    # __call__实现的是方法的调用时的动作，本处是view_func执行时的动作;
    def __call__(self, *args, **kwargs):
        # print "&" * 30
        return self.view(*args, **kwargs)

# 在app启动的时候，只加载LazyView的__init__方法,只有在有http请求的时候，才调用view方法，
# 这样可以让view在有http请求的时候才加载
app.add_url_rule('/hello',
                 view_func=LazyView('hello_app.views.hello'))


def hello():
    return "hello"


import os
from flask import send_from_directory


@app.route('/aa.jpg')
def favicon():
    # 提供展示静态文件方式，eg:图片，文件等
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'aa.jpg', mimetype='image/vnd.microsoft.icon')

# 返回流对象给客户端
from flask import Response, stream_with_context
# Response对象的初始化，可以是个字符串，也可以是个可迭代的对象；
# 如果是字符串，返回这个字符串，如果是可迭代对象，就返回迭代对象的全部的值
# stream_with_context生成器运行期间保持请求环境
@app.route('/large.csv')
def generate_large_csv():
    # 定义一个生成器，generate()象返回生成器对，generate().next返回每次yield的值
    # 但是，将生成器对象传回到Response中，将返回生成器生成的全部内容
    def generate():
        yield 'hello \n'
        yield 'world \n'
        yield '!'

    return Response(stream_with_context(generate()), mimetype='text/csv')


# 下面这段代码个人觉得比较帅，主要处理了在请求的时候如何保存response时要做的事
# 因为在请求的时候还没有response对象，所以用到了全局对象g，保存response时的动作

# 首先http请求发起前，执行detect_user_language方法,接着如果lanuage为None执行after_this_request这个装饰器函数，
# 将修饰的方法保存到g中，然后执行g.language=language
# 最后请求结束后，执行到after_request装饰的方法，获取g中存储的function，回调这些方法
def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f

@app.after_request
def call_after_request_callbacks(response):
    for callback in getattr(g, 'after_request_callbacks', ()):
        callback(response)
    return response


from flask import request


@app.before_request
def detect_user_language():
    language = request.cookies.get('user_lang3')
    if language is None:
        language = "zh_cn"

        @after_this_request
        def remember_language(response):
            response.set_cookie('user_lang3', language)
    g.language = language

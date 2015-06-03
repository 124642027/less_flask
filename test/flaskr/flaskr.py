#! /usr/bin/env python
#-*-coding:utf-8-*-
# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from contextlib import closing
import argparse
parser = argparse.ArgumentParser(description='run the app')
parser.add_argument('-e', '--env', type=str, help="choose environment", default="test")
args = parser.parse_args()

# create little application
app = Flask(__name__)

# app.config.from_object(__name__)
if args.env == "product":
    app.config.from_object('conf.product')
else:
    app.config.from_object('conf.test')

if not app.debug:
    import logging
    from logging import Formatter
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler(mailhost="smtp",
                               fromaddr="发件人",
                               toaddrs="收件人",
                               credentials=("username", "passwd"),
                               subject="youyou")
    mail_handler.setFormatter(Formatter("""
    Message type:          %(levelname)s
    Location:              %(pathname)s:%(lineno)d
    Module:                %(module)s
    Function:              %(funcName)s
    Time:                  %(asctime)s

    Message:
    %(message)s
    """
    ))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler("flaskr.log", maxBytes=1024000)
    file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()
    g.db.text_factory = str

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    g.db.close()

# @app.route('/')
# def show_entries():
#     cur = g.db.execute('select title, text from entries order by id desc')
#     entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
#     return render_template('show_entries.html', entries=entries)

from flask.views import View


class ShowEntries(View):
    """通用视图的例子,将视图方法的各个部分拆开，
    最主要的是dispatch_request和app.add_url_rule
    """
    methods = ['GET', 'POST']

    @property
    def get_template_name(self):
        """获取模块名称"""
        return 'show_entries.html'

    def render_template(self, context):
        """将context载入模板"""
        return render_template(self.get_template_name, **context)

    def get_objects(self):
        """获取数据表中数据"""
        cur = g.db.execute('select title, text from entries order by id desc')
        return [dict(title=row[0], text=row[1]) for row in cur.fetchall()]

    def dispatch_request(self):
        """将封装数据，并载入模板"""
        if request.method in ['POST', 'GET']:
            context = {'entries': self.get_objects()}
            return self.render_template(context)

# 动态的添加handler入口，和@router效果一致
app.add_url_rule('/', view_func=ShowEntries.as_view('show_entries'))

# 基于http方法(GET/POST)的调度,将http请求的方法和类中定义的方法匹配，做对应的动作，restfull api
'''
class UserAPI(MethodView):

    def get(self, user_id):
        if user_id is None:
            # 返回一个包含所有用户的列表
            pass
        else:
            # 显示一个用户
            pass

    def post(self):
        # 创建一个新用户
        pass

    def delete(self, user_id):
        # 删除一个用户
        pass

    def put(self, user_id):
        # update a single user
        pass

user_view = UserAPI.as_view('user_api')
app.add_url_rule('/users/', defaults={'user_id': None},
                 view_func=user_view, methods=['GET',])
app.add_url_rule('/users/', view_func=user_view, methods=['POST',])
app.add_url_rule('/users/<int:user_id>', view_func=user_view,
                 methods=['GET', 'PUT', 'DELETE'])
# default是参数的默认值
# methods是http请求的方法
# <int:user_id>指的是入参
'''

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get("logged_in"):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = "invalid username"
        elif request.form['password'] != app.config['PASSWORD']:
            error = "invalid password"
        else:
            session['logged_in'] = True
            flash("You are logged_in")
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    flash("You are logged out")
    return redirect(url_for('show_entries'))

"""
每当模板被渲染成功后，就会发送信号，执行connect调用的函数
"""
# template_rendered还渲染信号方法
from flask import template_rendered
# contextmanager是构造with使用结构的装饰器；以后想使用with返回一堆值，
# 然后最后进行收尾工作；可以使用这个装饰器
from contextlib import contextmanager

# 信号使用的简洁方式,每当模板渲染后执行print
# @template_rendered.connect_via(app)
# def when_template_rendered(app, template, context, **extra):
#     print 'Template %s is rendered with %s' % (template.name, context)

# 信号使用的原始方式
# @contextmanager
# def captured_templates(app):
#     recorded = []
#     def record(sender, template, context, **extra):
#         recorded.append((template, context))
#     template_rendered.connect(record, app)
#     try:
#         yield recorded
#     finally:
#         template_rendered.disconnect(record, app)
#
# with captured_templates(app) as templates:
#     rv = app.test_client().get('/')
#     assert rv.status_code == 200
#     assert len(templates) == 1
#     template, context = templates[0]
#     print template, context
#     assert template.name == 'show_entries.html'
#     assert len(context['entries']) > 0

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8683, debug=False)

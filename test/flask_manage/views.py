#! /usr/bin/env python
#-*-coding:utf-8-*-

import flask_admin as admin
from flask_manage import app


# Create custom admin view
class MyAdminView(admin.BaseView):
    @admin.expose('/')
    def index(self):
        return self.render('myadmin.html')


class AnotherAdminView(admin.BaseView):
    @admin.expose('/')
    def index(self):
        return self.render('anotheradmin.html')

    @admin.expose('/test/')
    def test(self):
        return self.render('test.html')


@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


# Create admin interface
admin = admin.Admin(name="Simple Views")
admin.add_view(MyAdminView(name="myadmin", category=u'分类'))
admin.add_view(MyAdminView(name="myadmin1", endpoint='test2', category=u'分类'))
admin.add_view(AnotherAdminView(name="otheradmin", category=u'分类'))
admin.init_app(app)
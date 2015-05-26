#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
测试Flask工程逻辑
包括登录，登出，添加等
测试的时候新建临时的数据库，初始化数据表结构；然后模拟流程
测试标准相当与验证flash内容，和页面返回数据内容
'''
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import unittest
import tempfile
import flaskr
import flask


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config["DATABASE"] = tempfile.mkstemp()
        flaskr.app.config["TESTING"] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post("/login", data = dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get("/logout", follow_redirects=True)

    def test_empty_db(self):
        rv = self.app.get("/")
        assert "No entries here so far" in rv.data

    def test_login_logout(self):
        rv = self.login("admin", 'default')
        assert 'You are logged_in' in rv.data
        rv = self.logout()
        assert 'You are logged out' in rv.data
        rv = self.login("adminx", 'default')
        assert 'invalid username' in rv.data

    def test_message(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(title='<hello>',
                                             text='<strong>HTML</strong>allow here'),
                           follow_redirects=True)
        assert "No entries here so far" not in rv.data
        assert '&lt;hello&gt;' in rv.data
        assert '<strong>HTML</strong>allow here' in rv.data


if __name__ == "__main__":
    unittest.main()

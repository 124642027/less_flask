#!/usr/env/bin python
# -*-coding:utf-8-*-

# use blueprint
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

# __name__ 当前文件的文件名
simple_page = Blueprint('simple_page', __name__, template_folder='templates')
print simple_page.root_path


@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template('show_entries.html')
    except TemplateNotFound:
        print "^" * 30
        abort(404)

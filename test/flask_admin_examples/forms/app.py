#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import os.path as op

from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.event import listens_for
from jinja2 import Markup

from flask_admin import Admin, form
from flask_admin.form import rules
from flask_admin.contrib import sqla


# Create application
app = Flask(__name__, static_folder='files')

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'files')
try:
    os.mkdir(file_path)
except OSError:
    pass


# Create models
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))

    def __unicode__(self):
        return self.name


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))

    def __unicode__(self):
        return self.name


class User(db.Model):
    __tablename__ = "user_forms"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Unicode(64))
    last_name = db.Column(db.Unicode(64))
    email = db.Column(db.Unicode(128))
    phone = db.Column(db.Unicode(32))
    city = db.Column(db.Unicode(128))
    country = db.Column(db.Unicode(128))
    notes = db.Column(db.UnicodeText)


# Delete hooks for models, delete files if models are getting deleted
# listens_for的第一个参数是监听的模板类名，第二个参数是控制删除顺序;在File类删除后执行删除文件操作
@listens_for(File, 'after_delete')
def del_file(mapper, connection, target):
    if target.path:
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass


@listens_for(Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass


# Administrative views
class FileView(sqla.ModelView):
    # Override form field to use Flask-Admin FileUploadField
    # 在添加和修改功能中添加上传文件功能，上传的路径存到path字段上
    form_overrides = {
        'path': form.FileUploadField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    # 重写form中字段的属性，这里重写字段的参数
    form_args = {
        'path': {
            'label': 'File',           # 上传文件的类型
            'base_path': file_path     # 上传文件存储的路径
        }
    }


class ImageView(sqla.ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        # Markup从jinjia2中引入，阻止自动转义
        return Markup('<img src="%s">' % url_for('static',
                                                 filename=form.thumbgen_filename(model.path)))

    # 格式化返回的字段的格式；此处将返回的图片地址格式化成html返回到页面
    # column_formatters被dict对象赋值，path返回的字段，_list_thumbnail格式化方法，这个方法固定有4个入参
    # 字段也可以添加如下限制dict(label='Big Text', validators=[validators.required()]，限制类型和是否必填
    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(100, 100, True))
    }


class UserView(sqla.ModelView):
    """
    This class demonstrates the use of 'rules' for controlling the rendering of forms.
    """
    # 定制弹出的form格式，定义fieldset，分类header和field
    form_create_rules = [
        # Header and four fields. Email field will go above phone field.
        rules.FieldSet(('first_name', 'last_name', 'email', 'phone'), 'Personal'),
        # Separate header and few fields
        rules.Header('Location'),
        rules.Field('city'),
        # String is resolved to form field, so there's no need to explicitly use `rules.Field`
        'country',
        # Show macro from Flask-Admin lib.html (it is included with 'lib' prefix)
        # 使用页面中定义的宏（macro）,rule_demo是在rule_create.html和rule_edit.html中引入的rule_demo.html页面的重命名
        # {% import 'rule_demo.html' as rule_demo %}这里使用rule_demo.warp方法，同时保证wrap方法中有{{ caller() }}
        # 表明可调用
        rules.Container('rule_demo.wrap', rules.Field('notes'))
    ]

    # Use same rule set for edit page
    form_edit_rules = form_create_rules

    create_template = 'rule_create.html'
    edit_template = 'rule_edit.html'


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

# Create admin
admin = Admin(app, 'Example: Forms')

# Add views
admin.add_view(FileView(File, db.session))
admin.add_view(ImageView(Image, db.session))
admin.add_view(UserView(User, db.session, name='User'))


def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import random
    import string

    db.drop_all()
    db.create_all()

    first_names = [
        'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie','Sophie', 'Mia',
        'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
        'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
    ]
    last_names = [
        'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
        'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
        'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
    ]
    locations = [
        ("Shanghai", "China"),
        ("Istanbul", "Turkey"),
        ("Karachi", "Pakistan"),
        ("Mumbai", "India"),
        ("Moscow", "Russia"),
        ("Sao Paulo", "Brazil"),
        ("Beijing", "China"),
        ("Tianjin", "China"),
        ("Guangzhou", "China"),
        ("Delhi", "India"),
        ("Seoul", "South Korea"),
        ("Shenzhen", "China"),
        ("Jakarta", "Indonesia"),
        ("Tokyo", "Japan"),
        ("Mexico City", "Mexico"),
        ("Kinshasa", "Democratic Republic of the Congo"),
        ("Bangalore", "India"),
        ("New York City", "United States"),
        ("London", "United Kingdom"),
        ("Bangkok", "Thailand"),
        ("Tehran", "Iran"),
        ("Dongguan", "China"),
        ("Lagos", "Nigeria"),
        ("Lima", "Peru"),
        ("Ho Chi Minh City", "Vietnam"),
        ]

    for i in range(len(first_names)):
        user = User()
        user.first_name = first_names[i]
        user.last_name = last_names[i]
        user.email = user.first_name.lower() + "@example.com"
        tmp = ''.join(random.choice(string.digits) for i in range(10))
        user.phone = "(" + tmp[0:3] + ") " + tmp[3:6] + " " + tmp[6::]
        user.city = locations[i][0]
        user.country = locations[i][1]
        db.session.add(user)

    images = ["Buffalo", "Elephant", "Leopard", "Lion", "Rhino"]
    for name in images:
        image = Image()
        image.name = name
        image.path = name.lower() + ".jpg"
        db.session.add(image)

    for i in [1, 2, 3]:
        file = File()
        file.name = "Example " + str(i)
        file.path = "example_" + str(i) + ".pdf"
        db.session.add(file)

    db.session.commit()
    return

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)

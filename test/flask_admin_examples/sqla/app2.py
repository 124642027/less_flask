#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import flask_admin as admin
from flask_admin.contrib import sqla


# Create application
app = Flask(__name__)


# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:root@localhost:3306/test'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(50))

    def __unicode__(self):
        return self.desc


class Tyre(db.Model):
    __tablename__ = 'tyres'
    tyre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), primary_key=True)
    # car_id和Car是外键关联，Tyre中的数据是依赖Car中的，这里添加relationship关系时给form用的
    # 这样form中返回car字段，就可以使用搜索功能，如果没有添加Car数据，car_id是不会被添加的
    car = db.relationship('Car')
    desc = db.Column(db.String(50))


class CarAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['desc',]


class TyreAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['car', 'tyre_id', 'desc']

# Create admin
admin = admin.Admin(app, name='Example: SQLAlchemy2')
admin.add_view(CarAdmin(Car, db.session))
admin.add_view(TyreAdmin(Tyre, db.session))

if __name__ == '__main__':

    # Create DB
    db.drop_all()
    db.create_all()

    # Start app
    app.run(debug=True)

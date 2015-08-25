#! /usr/bin/env python
# -*-coding:utf-8-*-
# 负责初始化app，导入视图模块，获取输入确定环境和logging配置

from flask import Flask


# create little application
app = Flask(__name__)

# 分割单个应用到一个大应用时，可以在__init__文件中导入所有视图和蓝图，但是这样做__init__.py文件会特别
# 长，导致不好维护，同时意义也不对；
# 此时，我们可以建立views.py逻辑处理文件，存储各种处理逻辑视图，在__init__.py文件中导入views即可
from flaskr import views

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

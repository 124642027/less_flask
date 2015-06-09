from flask import Flask

app = Flask(__name__)
app.debug = True

from hello_app import views

app.register_blueprint(views.bp, url_prefix='/<lang_code>')

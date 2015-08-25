from flask import Flask

# Create flask app
app = Flask(__name__, template_folder='templates')
app.debug = True

from flask_manage import views
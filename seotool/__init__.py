# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mongokit import Connection
from flask.ext.login import LoginManager
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = 'Please log in to access this page.'


from seotool import views, models


from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from seotool import app, lm, basedir
# from forms import LoginForm
# from models import User
# from config import MONGODB_HOST


@app.route('/')
@app.route('/index')
def index():
    #return basedir
    return render_template('index.html')
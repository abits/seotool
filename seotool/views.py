from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from seotool import app, db
from forms import LoginForm
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@login_required
@app.route('/accounts')
def accounts_list():
    return render_template('accounts.html')


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('accounts_list'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.users.User.one({'username': form.username.data})
        if user and user.check_password(form.password.data):
            session['remember_me'] = form.remember_me.data
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember=remember_me)
            user.last_login.date = datetime.utcnow()
            user.last_login.ip = request.remote_addr
            user.save()
            return redirect(url_for('accounts_list'))
        else:
            flash('Login failed! Password and user did not match.', 'error')
            return redirect('/login')
    return render_template('login.html', form=form)

@app.before_request
def before_request():
    g.user = current_user
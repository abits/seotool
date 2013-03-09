from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from seotool import app, db
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    #return basedir
    return render_template('index.html')

@login_required
@app.route('/dashboard')
def dashboard():
    return "hallo"


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.users.User.one({'username': form.username.data})
        if not user:
            flash('Login failed! Unknown user.', 'error')
        else:
            session['remember_me'] = form.remember_me.data
            if not user.check_password(form.password.data):
                flash('Login failed! Password does not match.', 'error')
            else:
                remember_me = False
                if 'remember_me' in session:
                    remember_me = session['remember_me']
                    session.pop('remember_me', None)
                login_user(user, remember=remember_me)
                return redirect(url_for('dashboard'))
        return redirect('/login')
    return render_template('login.html', form=form)

@app.before_request
def before_request():
    g.user = current_user
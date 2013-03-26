from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from seotool import app, db, tools
from forms import LoginForm
from datetime import datetime, date
from apiclient.discovery import build
from oauth2client.client import AccessTokenRefreshError, OAuth2Credentials
from apiclient.errors import HttpError
from httplib2 import Http
import json
import providers




@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@login_required
@app.route('/report/<account_id>')
def report(account_id):
    try:
        al = providers.Analytics()
        profile_id = al.get_profile_id(account_id)
        parameters = {
            'ids': profile_id,
            'start_date': date(2009, 3, 3),
            'end_date': date(2010, 3, 3),
            'metrics': 'visits',
            'dimensions': 'month'
        }
        data = al.retrieveData(parameters)
        chart_file = tools.render_line_chart(data)
    except providers.InvalidCredentialsError:
        data = {}
        chart_file = ''
        msg = '3 Please reauthorize the application to Google.'
        flash(msg)
        return redirect(url_for('profiles'))

    return render_template('report.html', data=data, chart_file=chart_file)


@login_required
@app.route('/profiles')
def profiles():
    try:
        credentials = OAuth2Credentials.from_json(json.dumps(g.user.credentials))
    except KeyError:
        credentials = None
    if credentials is None or credentials.invalid:
        return redirect(url_for('oauth_step1'))
    http = Http()
    try:
        http = credentials.authorize(http)
        service = build('analytics', 'v3', http=http)
    except AccessTokenRefreshError:
        msg = 'Please reauthorize the application to Google.'
        flash(msg)
    try:
        profiles = service.management().accounts().list().execute()
        print profiles
    except NameError:
        profiles = {}
    return render_template('profiles.html', profiles=profiles)


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
            return redirect(url_for('profiles'))
        else:
            flash('Login failed! Password and user did not match.', 'error')
            return redirect('/login')
    return render_template('login.html', form=form)


@app.route('/authorize')
def oauth_step1():
    authorize_url = app.config['FLOW'].step1_get_authorize_url()
    return redirect(authorize_url)


@app.route('/authorized')
def oauth_step_2():
    credentials = app.config['FLOW'].step2_exchange(request.args['code'])
    g.user.credentials = json.loads(credentials.to_json())
    g.user.save()
    return redirect(url_for('profiles'))


@app.before_request
def before_request():
    g.user = current_user
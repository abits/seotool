# -*- coding: utf-8 -*-
from flask.ext.wtf import Form, TextField, BooleanField, PasswordField
from flask.ext.wtf import Required, Length


class LoginForm(Form):
    username = TextField('Username', validators=[Required(), Length(max=32)])
    password = PasswordField('Password',
                             validators=[Required(), Length(max=32)])
    remember_me = BooleanField('Remember me', description="Remember me",
                               default=False)
# -*- coding: utf-8 -*-
from flask.ext.wtf import Form, TextField, BooleanField, PasswordField
from flask.ext.wtf import Required, Length, Email


class LoginForm(Form):
    username = TextField('Username', validators=[Required(), Length(max=32)])
    password = PasswordField('Password',
                             validators=[Required(), Length(max=32)])
    remember_me = BooleanField('Remember me', description="Remember me",
                               default=False)


class AccountAddForm(Form):
    account = TextField('Account', validators=[Email(
        message='Account must be a valid Google Mail Address.'),
                                               Length(max=64)])
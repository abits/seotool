# -*- coding: utf-8 -*-
# Forms module.  Represents HTML forms.
from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, TextAreaField, DateField
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


class ReportConfigurationForm(Form):
    summary = TextAreaField('Summary', validators=[Length(max=4096)])
    include_visitors = BooleanField('Visitors in time', description='Visitors in time', default=True)
    visitors_month = DateField('Visitors in month', description='Visitors in month')
    include_visitor_types = BooleanField('Visitor types', description='Visitor types', default=True)
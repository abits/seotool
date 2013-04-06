# -*- coding: utf-8 -*-
# Forms module.  Represents HTML forms.
from flask.ext.wtf import Form, \
    TextField, BooleanField, PasswordField, \
    TextAreaField, DateField, FormField, SelectField
from flask.ext.wtf import Required, Length, Email
from datetime import date


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


class VisitorsConfigurationForm(Form):
    include = BooleanField('Visitors', description='Visitors', default=True)
    month = SelectField('Month',
                        choices=[(x, y) for x, y in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], start=1)],
                        default=int(date.today().strftime('%m')),
                        coerce=int)
    year = SelectField('Year',
                       choices=[(x, str(x)) for x in reversed(range(1995,
                       int(date.today().strftime('%Y')) + 1))],
                       coerce=int)

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(VisitorsConfigurationForm, self).__init__(*args, **kwargs)


class ChartConfigurationForm(Form):
    visitors_for_month = FormField(VisitorsConfigurationForm)

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(ChartConfigurationForm, self).__init__(*args, **kwargs)


class ReportConfigurationForm(Form):
    summary = TextAreaField('Summary', validators=[Length(max=4096)])
    charts = FormField(ChartConfigurationForm)
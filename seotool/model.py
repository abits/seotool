# -*- coding: utf-8 -*-
# Model module.  This module contains model classes which abstract the persistence layer.
# It may also define transient data structures which hold generated data the services layer has to deal with.

import tools
from flask.ext.mongokit import Document
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import *


class User(Document):
    structure = {
        'username': unicode,
        'firstname': unicode,
        'lastname': unicode,
        'email': unicode,
        'pw_hash': basestring,
        'credentials': dict,
        'last_login': {
            'date': datetime,
            'ip': basestring
        },
        'created_at': datetime,
        'modified_at': datetime,
        'deleted_at': datetime,
    }
    validators = {
        'username': tools.max_length(50),
        'email': tools.max_length(120)
    }

    use_dot_notation = True
    use_autorefs = True

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def __repr__(self):
        return '<User: %r>' % self.username


class Report(Document):
    structure = {
        'profile_id': unicode,
        'last_author': User,
        'configuration': dict,
        'created_at': datetime,
        'modified_at': datetime,
        'deleted_at': datetime,
        'file': unicode
    }

    use_dot_notation = True
    use_autorefs = True


class BaseChart(object):
    data = []


class LineChart(BaseChart):

    def __init__(self, data):
        self.data = data

    def get_drawing(self):
        drawing = Drawing(600, 250)
        lc = HorizontalLineChart()
        lc.x = 50
        lc.y = 50
        lc.height = 250
        lc.width = 600
        lc.data = self.data
        lc.joinedLines = 1
        lc.categoryAxis.labels.boxAnchor = 'n'
        lc.valueAxis.valueMin = 0
        lc.valueAxis.valueMax = 2000
        lc.valueAxis.valueStep = 500
        lc.lines[0].strokeWidth = 2.5
        drawing.add(lc)
        return drawing






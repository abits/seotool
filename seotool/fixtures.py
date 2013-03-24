# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mongokit import Connection
from model import User
from datetime import datetime


app = Flask(__name__)
app.config.from_pyfile('../config.py')
connection = Connection(app.config['MONGODB_HOST'],
                       app.config['MONGODB_PORT'])
db = connection[app.config['MONGODB_NAME']]


def load():
    create_admin_user()


def create_admin_user():
    users = db.users
    if not users.one({'username': u'admin'}):
        connection.register(User)
        admin = users.User()
        admin.username = u'admin'
        admin.email = u'test_admin@localhost'
        admin.credentials = {}
        admin.firstname = u'Admin'
        admin.lastname = u'Admin'
        admin.created_at = datetime.utcnow()
        admin.modified_at = datetime.utcnow()
        admin.deleted_at = None
        admin.set_password('password')
        admin.save()

if __name__ == '__main__':
    load()
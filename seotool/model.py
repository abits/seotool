# -*- coding: utf-8 -*-
import tools
from flask.ext.mongokit import Document
from werkzeug.security import generate_password_hash, check_password_hash


class User(Document):
    structure = {
        'username': unicode,
        'email': unicode,
        'pw_hash': str,
        'accounts': dict
    }
    validators = {
        'username': tools.max_length(50),
        'email': tools.max_length(120)
    }

    use_dot_notation = True

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

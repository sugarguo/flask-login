#! usr/bin/python
#  -_-  coding:utf-8 -_-

'''
@author          sugarguo

@email           sugarguo@live.com

@date            2016年04月15日

@version         v1.0.0 

@copyright       Sugarguo

File             models.py

'''


from . import db
from . import login_manager

from datetime import datetime
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

    
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), unique = True, index = True)

    #recordings = db.relationship('Recording', backref = 'user')


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
    
    @property
    def password(self):
        raise AttributeError(u'禁止获取密码！')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User % r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

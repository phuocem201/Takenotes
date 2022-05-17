import os
from enum import unique
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db


SECRET_KEY = os.environ.get("KEY")



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150),unique = True)
    user_name = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(150))

    
    def __init__(self, email, password, user_name):
        self.email = email
        self.password = password
        self.user_name = user_name


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(SECRET_KEY, expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset(token):
        s = Serializer(SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        
        return User.query.get(user_id)

    
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
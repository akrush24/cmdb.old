from app import db, Base
from sqlalchemy import Column, Integer, String


ROLE_USER = 0
ROLE_ADMIN = 1

class Entries(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index = True, unique = False)
    text = db.Column(db.String(250), index = True, unique = False)
    addtext = db.Column(db.String(250), index = True, unique = False)

class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    
    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)
        
        
class Types(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(24), unique = True)
    
    def __init__(self, name=None):
        self.name = name 
from app import db, Base
from sqlalchemy import Column, Integer, String

ROLE_USER = 0
ROLE_ADMIN = 1

def _get_date():
    return datetime.datetime.now()


class Entries(db.Model): # For Test
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index = True, unique = False)
    text = db.Column(db.String(250), index = True, unique = False)
    addtext = db.Column(db.String(250), index = True, unique = False)

class Resources(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key = True)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    create_date = db.Column(db.DateTime)
    update_date = db.Column(db.DateTime)
    
    #create_date = db.Column(db.DateTime, default=_get_date())
    #update_date = db.Column(db.DateTime, onupdate=_get_date())

class Values(db.Model):
    __tablename__ = 'values'
    id = db.Column(db.Integer, primary_key = True)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'))
    res_id = db.Column(db.Integer, db.ForeignKey('resources.id'))
    value = db.Column(db.String(250), index = True, unique = False)
    update_date = db.Column(db.DateTime)
    #lase = db.Column(db.tinyint(1))

class Types(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(24), unique = True)
    
    def __init__(self, name=None):
        self.name = name 

class Options(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    front_page = db.Column(db.Integer)

class Dict(db.Model):
    __tablename__ = 'dict'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = False)

class Dict_Val(db.Model):
    __tablename__ = 'dict_val'
    id = db.Column(db.Integer, primary_key = True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict.id'))
    name = db.Column(db.String(255), unique = False)
    

    
#
class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(255))
    
    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

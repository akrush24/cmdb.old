from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class entries(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index = True, unique = False)
    text = db.Column(db.String(250), index = True, unique = False)
    addtext = db.Column(db.String(250), index = True, unique = False)

class users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(24), index = True, unique = True)
    passwd = db.Column(db.String(64), index = True, unique = False)
    

class Type(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(24), index = True, unique = True)
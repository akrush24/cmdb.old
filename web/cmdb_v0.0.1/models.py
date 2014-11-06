from app import db, Base
from sqlalchemy import Column, Integer, String


class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    hash = db.Column(db.Integer)
    resid=db.Column(db.Integer)
    user = db.Column(db.String(50))
    create_date = db.Column(db.DateTime)
    update_date = db.Column(db.DateTime)


class Value(db.Model):
    __tablename__ = 'value'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'))
    res_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    value = db.Column(db.String(250), index = True, unique = False)
    update_date = db.Column(db.DateTime)
    #lase = db.Column(db.tinyint(1), )


class Types(db.Model):
    __tablename__ = 'types'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(24), unique = True)
    workflow =  db.Column(db.Integer, db.ForeignKey('workflow_s.id'))
    desc = db.Column(db.String(244))
    

class Options(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(100), unique = False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    description = db.Column(db.String(100), unique = False)
    option_type = db.Column(db.String(10), unique = False)
    user_visible = db.Column(db.Integer)
    front_page_visible = db.Column(db.Integer)
    required = db.Column(db.Integer)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict.id'))


class Dict_s(db.Model):
    __tablename__ = 'dict_s'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(100), unique = True)


class Dict(db.Model):
    __tablename__ = 'dict'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict.id'))
    value = db.Column(db.String(100))


class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True)
    full_name = Column(String(150), unique=False)
    email = Column(String(120), unique=True)
    password = Column(String(255))
    last_activity = db.Column(db.DateTime)


class WorkFlow_s(db.Model):
    __tablename__ = 'workflow_s'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(250), unique=True)


class WorkFlow(db.Model):
    __tablename__ = 'workflow'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(250))
    step =  db.Column(db.Integer, db.ForeignKey('workflow.id'))

# score - таблица содержит последний номер Итема по определенному Типу
class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    type_id =  db.Column(db.Integer, db.ForeignKey('types.id'), unique = True)
    score = Column(Integer)


# relation - таблица содержит соотношение Типа и Опции
class Relation(db.Model):
    __tablename__ = 'relation'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), unique = True)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'), unique = True)




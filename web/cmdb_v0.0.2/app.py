#! /usr/bin/env python
# -*- coding: utf-8 -*-

# All Imports
from __future__ import unicode_literals
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
import simplejson
from sqlalchemy.sql import select
import re
import peppercorn

from flaskext.mysql import MySQL

import actions
import hashlib

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


mysql = MySQL()

app = Flask(__name__)
app.config.from_object('config')

app.config['MYSQL_DATABASE_USER'] = 'cmdb'
app.config['MYSQL_DATABASE_PASSWORD'] = 'unix11'
app.config['MYSQL_DATABASE_DB'] = 'cmdb_v.0.0.2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

import models
from models import *
    
#def init_db():
    # Здесь нужно импортировать все модули, где могут быть определены модели,
    # которые необходимым образом могут зарегистрироваться в метаданных.
    # В противном случае их нужно будет импортировать до вызова init_db()
    #Base.metadata.create_all(bind=engine)

 
def cols_name(query):
    db = get_db()
    cur = db.execute(query)
    #keyst = list(map(lambda x: x[0], cur.description))  
    return ""

##############################################
# Decoration
#

#......................................................#
#### Обработка Типов ####
@app.route('/new_type/', methods=['GET', 'POST'])
def new_type():
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    db.execute('''insert into types (name) values (%s)''', request.form['name'])
    
    return redirect(url_for('control'))

@app.route('/del_type/<int:id>', methods=['GET'])
def del_type(id):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    db.execute('delete from types where id=%s', [id])


    return redirect(url_for('control'))

@app.route('/get_list_type/')
def get_list_type():
    db = get_db()
    cur = db.execute('select * from types order by id desc')
    entries = cur.fetchall()
    json_row=[]
    for en in entries:
        json_row.append(dict(en))
    
    return simplejson.dumps(json_row,sort_keys=True,indent=4)
    
#......................................................#
#### Обработка свойств\опций ####

# 1. Добавление
# 2. Редактирование
@app.route('/new_option/', methods=['GET', 'POST'])
def new_option():
    if not session.get('logged_in'):
        abort(401)
    test=""
    db = get_db()
    for data in request.form.keys():
        value=request.form[data]
        if data != "type_id" and data[:5] != "newid" and value != "":
            option_id = data[2:]
            
            cur = db.execute('update options set name=%s where id=%s', value, option_id)

            test=test+option_id+' = '+value+'; '
            
        if data[:5] == "newid" and value != "":
            db.execute('insert into options (name, type_id) values (%s, %s)', [value, request.form['type_id']])
            test=test+'NEWID: '+data[:5]+'='+value+'; '

    
    #return test
    return redirect(url_for('control'))

@app.route('/del_option/<int:id>', methods=['GET'])
def del_option(id):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    db.execute('delete from options where id=%s', [id])
    
    return redirect(url_for('control'))

@app.route('/get_list_option/', methods=['GET'])
def get_list_option():
    type = request.args.get('type')
    db = get_db()
    if type is not None:
        cur = db.execute('select * from options where type_id = %s order by id desc', [type])
    else:
        cur = db.execute('select * from options order by id desc')
        
    entries = cur.fetchall()
    json_row=[]
    for en in entries:
        json_row.append(dict(en))
    
    return simplejson.dumps(json_row)


#......................................................#
#### Обработка пользователей ####
@app.route('/new_user/', methods=['GET', 'POST'])
def new_user():
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    db.execute('insert into users (login, full_name, email, password) values (%s, %s, %s, %s)',
                [request.form['login'], request.form['full_name'], request.form['email'], request.form['password']] )
    
    return redirect(url_for('control'))

@app.route('/del_user/<int:id>', methods=['GET'])
def del_user(id):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    db.execute('delete from users where id=%s', [id])

    return redirect(url_for('control'))

@app.route('/get_list_user/', methods=['GET'])
def get_list_user():
    username = request.args.get('email_list')
    db = get_db()
    if username is not None:
        cur = db.execute( 'select * from users WHERE upper(full_name) like '+username+' order by id desc' )
        #cur = db.execute( 'select * from users WHERE upper(full_name) like upper("%'+user+'%") or upper(login) like upper("%'+user+'%") order by id desc' )
    else:
        cur = db.execute('select * from users order by id desc limit 10')
    entries = cur.fetchall()
    json_row=[]
    for en in entries:
        json_row.append(dict(en))
    
    return simplejson.dumps(json_row)


########################################################################
##### Главная страница #################################################
@app.route('/list/<typename>/')
@app.route('/', defaults={'typename': None})
def index(typename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db=get_db()
    
    u = db.execute('select * from users')
    #return u
   
    return render_template( 'index.html', entries=u, cols_names="", user=session['login'] )

@app.route('/add', methods=['POST'])
def add():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (%s, %s)', [request.form['title'], request.form['text']])

    flash('New entry was successfully posted')
    return redirect(url_for('index'))


@app.route('/edit/<int:entry_id>')
def edit(entry_id):
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    cur = db.execute('select * from entries where id=%s', [entry_id])
    entries = cur.fetchall()
    keys=entries[0].keys()
    return render_template('edit.html', entries=entries, keys=keys, user=session['login'])


@app.route('/del/<int:entry_id>', methods=['GET'])
def delete(entry_id):
    if not session.get('logged_in'):
        abort(401)
    db = get_db()

    flash('Entry ? deleted', [entry_id])
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
 
    if request.method == 'POST':
        db = get_db()
        entries = db.execute('select * from users where login=%s limit 1', [request.form['login']] ).fetchall()
        
        for password in entries:
            user_password = entries[0][2]
            if request.form['password'] == user_password:
                session['logged_in'] = True
                session['login']=request.form['login']
                flash('You were logged in')
                return redirect(url_for('index'))

        if g.user is None:
            error = "Invalid User or Password"

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('login', None)
    #flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/control/', defaults={'action': "0"})
@app.route('/control/<action>')
def control(action):
    if not session.get('logged_in'):
        return redirect(url_for('login'))   
    db = get_db()

    type_cols = db.execute('select * from types order by id desc').fetchall()

    query = 'select * from options'
    option_cols = db.execute(query).fetchall()

    user_cols = db.execute('select * from users order by id desc').fetchall()

    return render_template('control.html', 
        type_cols=type_cols, type_cols_names=cols_name('select * from types order by id desc'), 
        option_cols=option_cols, option_cols_names = cols_name(query),
        user_cols = user_cols, user_cols_names=cols_name('select * from users order by id desc'),
        user=session['login']
    )



@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html', user=session['login'])

@app.route('/test-json', methods=['GET', 'POST'])
def testjson():
    db = get_db()
    cur = db.execute('select * from types order by id desc')
    entries = cur.fetchall()
    json_row=[]
    for en in entries:
        json_row.append(dict(en))
    return simplejson.dumps(json_row)



import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/newres', methods=['GET', 'POST'])
def newres():
    UUID = id_generator(6,"abcdefghijklmnopqrstuvwxyz0123456789")
    
    try:
        db = get_db()
        db.execute('insert into resources (hash, type_id) values (?, ?)', [UUID, request.form['type_id']])
        
    
        res_id=db.execute('select id from resources where hash=? limit 1', [UUID]).fetchall()[0][0]
        #res_id = entries

        for data in request.form.keys():
            if data != "type_id":
                option_id = data[2:]
                value=request.form[data]
                cur = db.execute('insert into value (option_id, value, res_id) values (?, ?, ?)', [option_id, value, res_id])

        
    except:
        flash('Unexpected ERROR')

    return redirect(url_for('index'))






#############################################################
# DB 
#\
'''
def connect_db():
    db_conn = MySQL.connect(host='localhost',user='cmdb',passwd='unix11',db='cmdb_v.0.0.2')
    return db_conn
    # DB connect
    #rv = sqlite3.connect(app.config['DATABASE'])
    #rv.row_factory = sqlite3.Row
    #return rv

@app.before_request
def db_connect():
    g.db = connect_db()
    return g.db
'''

def get_db():
    #
    #if not hasattr(g, app.config['DATABASE']):
    #    g.sqlite_db = connect_db()
    return engine


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(app.config['DATABASE'], mode='r') as f:
            db.cursor().executescript(f.read())

'''
@app.teardown_appcontext
def close_db(error):

    g.db.close()
'''
    
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


#############################################
# App RUN
#
if __name__ == '__main__':
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'], port=40000)


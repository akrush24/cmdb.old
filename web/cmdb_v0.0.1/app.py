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

import actions
import hashlib

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

import models
from models import *
    
def init_db():
    # Здесь нужно импортировать все модули, где могут быть определены модели,
    # которые необходимым образом могут зарегистрироваться в метаданных.
    # В противном случае их нужно будет импортировать до вызова init_db()
    Base.metadata.create_all(bind=engine)

 
def cols_name(query):
    db = get_db()
    cur = db.execute(query)
    keyst = list(map(lambda x: x[0], cur.description))  
    return keyst

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
    db.execute('insert into types (name) values (?)',
                [request.form['name']])
    db.commit()
    
    return redirect(url_for('control'))

@app.route('/del_type/<int:id>', methods=['GET'])
def del_type(id):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    db.execute('delete from types where id=?', [id])
    db.commit()

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
            
            cur = db.execute('update options set name=? where id=?', [value, option_id])

            test=test+option_id+' = '+value+'; '
            #q="insert into value (option_id, value, res_id) values ("+option_id+", "+value+", "+res_id+"); "+q
            
        if data[:5] == "newid" and value != "":
            db.execute('insert into options (name, type_id) values (?, ?)', [value, request.form['type_id']])
            #db.commit()
            test=test+'NEWID: '+data[:5]+'='+value+'; '

    db.commit()
    
    #return test
    return redirect(url_for('control'))

@app.route('/del_option/<int:id>', methods=['GET'])
def del_option(id):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    db.execute('delete from options where id=?', [id])
    db.commit()
    
    return redirect(url_for('control'))

@app.route('/get_list_option/', methods=['GET'])
def get_list_option():
    type = request.args.get('type')
    db = get_db()
    if type is not None:
        cur = db.execute('select * from options where type_id = ? order by id desc', [type])
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
    db.execute('insert into users (login, full_name, email, password) values (?, ?, ?, ?)',
                [request.form['login'], request.form['full_name'], request.form['email'], request.form['password']] )
    db.commit()
    
    return redirect(url_for('control'))

@app.route('/del_user/<int:id>', methods=['GET'])
def del_user(id):
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    db.execute('delete from users where id=?', [id])
    db.commit()

    return redirect(url_for('control'))

@app.route('/get_list_user/', methods=['GET'])
def get_list_user():
    username = request.args.get('email_list')
    db = get_db()
    if username is not None:
        cur = db.execute( 'select * from users WHERE upper(full_name) like upper("%'+username+'%") order by id desc' )
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

    val2=[]
    if typename is not None:

        db = get_db()
        
        try:
            typeid=db.execute('select id from types where name=?',[typename]).fetchall()[0][0]
        except IndexError:
            typeid=None

        count_resources=db.execute('select resources.id, hash from resources where resources.type_id=?',[typeid]).fetchall()

        
        for res_id, hash in count_resources:

            entries=db.execute('select id,name from options where type_id=?',[typeid]).fetchall()
            key=['UUID']
            val=[hash]
            for opt_id, v in entries:
                try:
                    key.append(v)
                except:
                    key.append("")
                    
                entries=db.execute('select value from value where res_id=? and option_id=?', [res_id, opt_id]).fetchall()
                        
                try:
                    val.append(entries[0][0])
                except:
                    val.append("")
                    
            val2.append(val)
        try:
            return render_template( 'index.html', entries=val2, cols_names=key, user=session['login'] )
        except:
            return render_template( 'index.html', entries="", cols_names="", user=session['login'] )
    
   
    return render_template( 'index.html', entries="", cols_names="", user=session['login'] )

@app.route('/add', methods=['POST'])
def add():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    if not session.get('logged_in'):
        abort(401)
    
    f = request.form
    query = 'update entries set '
    i=0
    keys=[]
    value=[]
    for key in f.keys():
        if key != 'id':
            if len(f.keys())-1 > i:
                query = query+key+', '
                keys.append(key)
                value.append(f[key])
            else:
                query = query+'%s=? '
                keys.append(key)
                value.append(f[key])
            i = i+1

    query = query+'where id='+f.getlist('id')[0]
    #return (query)
    
    query = 'update entries set {0}={2}, {1}=?, {2}=? where id=4'
    #return ( query  % f.keys()[0], f.keys()[1], f.keys()[2] )
    #keys = ['wr','ret','qwqw']
    return ( query.format(*keys) )
    db = get_db()
    #db.execute( ('update entries set %s=?' % f.keys()[1] ),[ f[f.keys()[1]] ])
    #db.execute( (query % f.keys()[0], f.keys()[1], f.keys()[2]) , [ f[f.keys()[0]], f[f.keys()[1]], f[f.keys()[2]] ])
    db.commit()
    

    #return redirect(url_for('index'))

@app.route('/edit/<int:entry_id>')
def edit(entry_id):
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    cur = db.execute('select * from entries where id=?', [entry_id])
    entries = cur.fetchall()
    keys=entries[0].keys()
    return render_template('edit.html', entries=entries, keys=keys, user=session['login'])


@app.route('/del/<int:entry_id>', methods=['GET'])
def delete(entry_id):
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('delete from entries where id=?', [entry_id])
    db.commit()
    flash('Entry ? deleted', [entry_id])
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
 
    if request.method == 'POST':
        db = get_db()
        entries = db.execute('select * from users where login=? limit 1', [request.form['login']] ).fetchall()
        
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

    #cur = db.execute('select * from options order by id desc')
    #query = 'select options.id, options.name, types.name, options.front_page, options.opttype, options.description, options.user_visible, options.required from options, types where options.type_id = types.id'
    query = 'select * from options'
    option_cols = db.execute(query).fetchall()

    user_cols = db.execute('select * from users order by id desc').fetchall()

    return render_template('control.html', 
        type_cols=type_cols, type_cols_names=cols_name('select * from types order by id desc'), 
        option_cols=option_cols, option_cols_names = cols_name(query),
        user_cols = user_cols, user_cols_names=cols_name('select * from users order by id desc'),
        user=session['login']
    )

    #cur = db.execute('select * from users order by id desc')
    #user_cols = cur.fetchall()
    #return render_template('control.html', type_cols=type_cols, type_cols_names=cols_name('types'), option_cols=option_cols, option_cols_names = cols_name('options'))


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
        db.commit()
    
        res_id=db.execute('select id from resources where hash=? limit 1', [UUID]).fetchall()[0][0]
        #res_id = entries

        for data in request.form.keys():
            if data != "type_id":
                option_id = data[2:]
                value=request.form[data]
                cur = db.execute('insert into value (option_id, value, res_id) values (?, ?, ?)', [option_id, value, res_id])

        db.commit()
        
    except:
        flash('Unexpected ERROR')

    return redirect(url_for('index'))






#############################################################
# DB 
#
def connect_db():
    # DB connect
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
def get_db():
    #
    if not hasattr(g, app.config['DATABASE']):
        g.sqlite_db = connect_db()
    return g.sqlite_db
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(app.config['DATABASE'], mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
@app.teardown_appcontext
def close_db(error):
    '''Closes the database again at the end of the request.'''
    if hasattr(g, app.config['DATABASE']):
        g.sqlite_db.close()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


#############################################
# App RUN
#
if __name__ == '__main__':
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'])


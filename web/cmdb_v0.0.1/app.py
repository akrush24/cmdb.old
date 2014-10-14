#! /usr/bin/env python

# All Imports
from __future__ import unicode_literals
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
import simplejson


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import models

def cols_name(table_name):
    db = get_db()
    cur = db.execute('PRAGMA table_info(%s)' % table_name)
    col = cur.fetchall()
    keyst=[]
    for c in col:
        keyst.append(c[1])    
    return keyst

##############################################
# Decoration
#
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    cur = db.execute('select * from entries order by id desc')
    entries = cur.fetchall()
    keys=entries[0].keys()
  
    return render_template('index.html', entries=entries, keys=cols_name('entries'))

@app.route('/json/')
def json():
    db = get_db()
    cur = db.execute('select * from entries order by id desc')
    entries = cur.fetchall()
    json_row=[]
    for en in entries:
        json_row.append(dict(en))
    #return jsonify(table=json_row)
    return simplejson.dumps(json_row)
    #return json.dumps(dict(entries[0]),dict(entries[1]),dict(entries[2]),dict(entries[3]),dict(entries[4]))

@app.route('/ang/')
def ang():
    return app.send_static_file('ang.html')


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
    #db = get_db()
    #db.execute('update entries set title=?, text=? where id=?',[request.form['title'], request.form['text'], request.form['id']])
    #db.commit()
    q='update entries set '
    set_cols_name=cols_name('entries')

    return('%s, %s' % set_cols_name[0], set_cols_name[1])
    #return redirect(url_for('index'))

@app.route('/edit/<int:entry_id>')
def edit(entry_id):
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    cur = db.execute('select * from entries where id=?', [entry_id])
    entries = cur.fetchall()
    keys=entries[0].keys()
    return render_template('edit.html', entries=entries, keys=keys)


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
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            #flash('You were logged in')
            g.user = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    #flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/control/')
def control():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('control.html')



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


#############################################
# App RUN
#
if __name__ == '__main__':
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'])


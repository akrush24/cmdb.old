#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# all the imports

from __future__ import with_statement
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import sqlite3

# configuration
DATABASE = '/home/cmdb/db/cmdb.sqlite'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def show_entries():
    cur = g.db.execute('SELECT ilogin,pass FROM users')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    #return render_template('show_entries.html', entries=entries)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
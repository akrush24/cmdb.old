#!flask/bin/python

# Все зависимости
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

# Конфигурация
DATABASE = os.path.join(app.root_path, 'cmdb.sqlite')
DEBUG = True
SECRET_KEY = 'key'
USERNAME = 'admin'
PASSWORD = 'default'
HOST='0.0.0.0'

app.config.from_object(__name__)

# Декораторы
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    cur = db.execute('select * from entries order by id desc')
    entries = cur.fetchall()
    keys=entries[0].keys()
    return render_template('index.html', entries=entries, keys=keys)

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
    db = get_db()
    db.execute('update entries set title=?, text=? where id=?',
                [request.form['title'], request.form['text'], request.form['id']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

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
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/control/')
def control():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('control.html')

def connect_db():
# Соединяет с указанной базой данных
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    '''Если ещё нет соединения с базой данных, открыть новое - для
    текущего контекста приложения
    '''
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

# Запуск 
if __name__ == '__main__':
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'])

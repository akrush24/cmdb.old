#! /usr/bin/env python
# -*- coding: utf-8 -*-

# All Imports
from __future__ import unicode_literals
import os, sys, ldap, datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
import simplejson
import re
import string, random
from functools import wraps
import hashlib, uuid
import cgitb, csv, math

from werkzeug import secure_filename

now = datetime.datetime.now()

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config.from_object('config')

LDAP_SERVER = "192.168.10.2"
LDAP_PORT = 389 # your port

db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from models import *

#import view
 
def cols_name(query):
    db = get_db()
    cursor = db.execute(query)
    return list( cursor.keys())

##############################################
# Decoration
#

#......................................................#
#### Обработка Типов ####
@app.route('/new_type/', methods=['POST'])
def new_type():
   
    db = get_db()
    try:
        db.execute('''insert into types (name) values (%s)''', request.form['name'].upper())
    except:
        flash('Ошибка, проверьте что имена типов не совпадают')
    return redirect(url_for('control'))

@app.route('/del_type/<int:id>', methods=['GET'])
def del_type(id):
    try:
        db = get_db()
        db.execute('delete from types where id=%s', [id])
    except:
       flash('This parameter is used!') 
        
    return redirect(url_for('control'))
    
@app.route('/clear_type/<int:id>')
def clear_type(id):

    try:
        db = get_db()
        db.execute('delete from value where res_id in (select id from resources where type_id=%s)', [id])
        db.execute('delete from resources where type_id=%s', [id])
        
        flash('Данные почищены')
    except:
       flash('This parameter is used!')
        
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

@app.route('/get_user_menu/')
def get_user_menu():
    
    db = get_db()
    cur = db.execute('select id, name from types order by id desc')
    entries = cur.fetchall()
    json_row=[]
    
    for en in entries:
        value=db.execute('select count(id) from resources where type_id=%s', [en[0]]).fetchall()[0][0]
        json_row.append(dict(en, value=value))
        
    #return en[1]
    return simplejson.dumps(json_row,sort_keys=True,indent=4)

#......................................................#
#### Обработка свойств\опций ####

# 1. Добавление
# 2. Редактирование
# 3. Очистка данных
@app.route('/new_option/', methods=['GET', 'POST'])
def new_option():

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

@app.route('/del_option/<int:id>')
def del_option(id):

    try:
        db = get_db()
        db.execute('delete from options where id=%s', [id])
    except:
       flash('This parameter is used!', 'error') 
            
    return redirect(url_for('control'))

@app.route('/clear_option/<int:id>')
def clear_option(id):
    
    if not session.get('logged_in'):
        abort(401)
    
    try:
        db = get_db()
        db.execute('delete from value where option_id=%s', [id])
        
        flash('Данные почищены')
    except:
       flash('This parameter is used!')
        
    return redirect(url_for('control'))

@app.route('/get_list_option/', methods=['GET'])
def get_list_option():
    
    type_id = request.args.get('type')
    opt_id = request.args.get('opt_id')
    db = get_db()
    if type_id is not None:
        cur = db.execute('select * from options where type_id = %s order by id desc', [type_id])
    elif opt_id is not None:
        cur = db.execute('select * from options where id = %s order by id desc', [opt_id])
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

    db = get_db()
    db.execute('insert into users (login, full_name, email, password) values (%s, %s, %s, %s)',
                [request.form['login'], request.form['full_name'], request.form['email'], hashlib.sha512(request.form['password']).hexdigest()]  )
    
    return redirect(url_for('control'))

@app.route('/del_user/<int:id>', methods=['GET'])
def del_user(id):

    db = get_db()
    db.execute('delete from users where id=%s', [id])

    return redirect(url_for('control'))

@app.route('/get_list_user/', methods=['GET'])
def get_list_user():
    
    username = request.args.get('email_list')
    db = get_db()
    if username is not None:
        cur = db.execute( 'select login, full_name from users WHERE upper(full_name) like upper(%s) order by id desc', username+'%' )
        #cur = db.execute( 'select * from users WHERE upper(full_name) like upper("%'+user+'%") or upper(login) like upper("%'+user+'%") order by id desc' )
    else:
        cur = db.execute('select login, full_name from users order by id desc limit 10')
    entries = cur.fetchall()
    json_row=[]
    for en in entries:
        json_row.append(dict(en))
    
    return simplejson.dumps(json_row)



#......................................................#
#### Обработка Словарей ####
@app.route('/new_dict/', methods=['POST'])
def new_dict():
    
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    if request.form['name'] != "":
        try:
            db.execute('insert into dict (name) values (%s)', request.form['name'])
            for data in request.form.keys():
                value=request.form[data]
                if data != "name" and data[:5] == "newid" and value != "":
                    db.execute('insert into dict_val (dict_id, value) values ((select id from dict where name=%s), %s)', [request.form['name'],value])
        except:
            flash ("Ошибка при добавлении словаря")
    return redirect(url_for('control'))


@app.route('/del_dict/<int:id>')
def del_dict(id):
    
    if not session.get('logged_in'):
        abort(401)

    db = get_db()
    db.execute('delete from dict_val where id=%s', [id])

    return redirect(url_for('control'))

@app.route('/get_list_dict/', methods=['GET'])
def get_list_dict():
    
    dict_id = request.args.get('dict_id')
    db = get_db()
    
    
    if dict_id is not None:
        cur = db.execute('select dict_val.id as val_id, dict.id, dict.name, dict_val.value from dict, dict_val where  dict.id=dict_val.dict_id and dict.id=%s', dict_id)
    else:
        cur = db.execute('select dict_val.id as val_id, dict.id, dict.name, dict_val.value from dict, dict_val where dict.id=dict_val.dict_id')
    
    entries = cur.fetchall()
    json_row=[]
    for en in entries:
        json_row.append(dict(en))
    
    return simplejson.dumps(json_row,sort_keys=True, indent=4)


#......................................................#
#### Обработка Ресурсов ####

# Удаление..............................................
@app.route('/del/<typename>/<hash>')
def del_res(hash, typename):

    db = get_db()
    
    db.execute('delete from value where res_id in (SELECT id FROM resources Where hash=%s)', [hash])
    db.execute('delete from resources where hash=%s', [hash])
    
    return redirect(url_for('index', typename=typename))

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Создание..............................................
def addres(type_id): # добавляем новый элемент в таблицу Resources
    UUID = id_generator(4,"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    # 4 - 1 679 616
    # 5 - 60 466 176
    # 6 - 2 176 782 336
    
    db = get_db()
        
    ALL_HASH=db.execute('select hash from resources').fetchall()
    hashs=[]
        
    for h in ALL_HASH:
        hashs.append(h)
        
    if UUID is not hashs:
        pass
    else:
        UUID = id_generator(6,"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        
    db.execute('insert into resources (hash, type_id, user, create_date) values (%s, %s, %s, %s)', [UUID, type_id, session['login'], datetime.datetime.now() ])
    res_id=db.execute('select id from resources where hash=%s limit 1', [UUID]).fetchall()[0][0]
    return res_id

@app.route('/newres', methods=['POST'])
def newres():
    
    try:
        db = get_db()
        typename = db.execute('select name from types where id=%s', [request.form['type_id']]).fetchall()[0][0]
        res_id=addres(request.form['type_id'])
        
        #return str(res_id)
        for data in request.form.keys():
            if data != "type_id":
                option_id = data[2:]
                value=request.form[data]
                cur = db.execute('insert into value (option_id, value, res_id) values (%s, %s, %s)', [option_id, value, res_id])

    except:
        flash('Unexpected ERROR')

    return redirect(url_for('index', typename=typename))

# Редактирование.............................................
@app.route('/editres', methods=['GET', 'POST'])
def editres():
    
    try:
        db = get_db()
        typename = db.execute('select name from types where id=%s', [request.form['type_id']]).fetchall()[0][0]
        res_id=addres(request.form['type_id'])
        
        #return str(res_id)
        for data in request.form.keys():
            if data != "type_id":
                option_id = data[2:]
                value=request.form[data]
                cur = db.execute('insert into value (option_id, value, res_id) values (%s, %s, %s)', [option_id, value, res_id])

    except:
        pass
        
    return request.form['uuid']

    #return redirect(url_for('index', typename=typename))


# Страница просмотра Итема
@app.route('/hash/<hash>/')
@app.route('/item/<hash>/')
def view(hash):
    
    if hash != "":
        res_id, type_id, type_name = engine.execute('select resources.id, types.id, types.name from resources, types where hash=%s limit 1',[hash]).fetchall()[0]
        try:
            (res_id, type_id, type_name)=engine.execute('select resources.id, types.id, types.name from resources, types where hash=%s',[hash]).fetchall()[0][0]
            return type_name
        except:
            res_id=None
        
        items=[]
        if res_id is not None:
            options=engine.execute('select id, name from options where type_id in (select type_id from resources where hash=%s)',[hash]).fetchall()
            for option_id, option_name in options:
                try:
                    value=engine.execute('select value from value where res_id in (select id from resources where hash=%s) and option_id=%s', [hash, option_id] ).fetchall()[0][0]
                except:
                    value=""
                    
                items.append(dict(id=option_id, option=option_name, value=value))
                
            #return str(item)
        
            return render_template('view.html', items=items)
            
        else: # если ресурса не существует
            return render_template( 'view.html')

 
# ..........................................................................
##### Главная страница .................................................####
@app.route('/list/<typename>/<int:page>/')
@app.route('/list/<typename>/', defaults={'page': 1})
@app.route('/', defaults={'typename': None, 'page': 1})
def index(typename, page):
    
    val2=[]
    json_row=[]
    json_col=[]
    json_row2=[]

    if typename is not None:
        uuid = request.args.get('uuid')
        db = get_db()
        try:
            typeid=db.execute('select id from types where name=%s',[typename]).fetchall()[0][0]
        except IndexError:
            typeid=None
            return render_template( 'index.html', entries="", cols_names="", typename=typename)



        if uuid is not None:
            resources=db.execute('select resources.id, hash from resources where BINARY resources.hash=%s and resources.type_id=%s', [uuid, typeid]).fetchall()
            count=db.execute('select count(id) from resources where resources.type_id=%s',[typeid]).fetchall()[0][0] # число ресурсов по выбранному типу
        elif request.args.get('save') is not None:
            resources=db.execute('select resources.id, hash from resources where resources.type_id=%s order by id desc',[typeid]).fetchall()
            count=db.execute('select resources.id, hash from resources where resources.type_id=%s order by id desc',[typeid]).fetchall()[0][0] # число ресурсов по выбранному типу
        else:
            ROW_IN_PAGE=30 # Число строк на одну таблицу
            COUNT_RES=db.execute('select count(id) from resources where resources.type_id=%s',[typeid]).fetchall()[0][0] # число ресурсов по выбранному типу
            
            if COUNT_RES != 0:
                COUNT_PAGE=round(COUNT_RES/ROW_IN_PAGE+0.5, 0)
            else:
                COUNT_PAGE=0
            COUNT_PAGE=int(COUNT_PAGE)
                
            resources=db.execute('select resources.id, hash from resources where resources.type_id=%s order by id desc LIMIT %s, %s',
            [typeid, (page-1)*ROW_IN_PAGE, ROW_IN_PAGE ] ).fetchall()
            

            count=COUNT_RES-(page-1)*ROW_IN_PAGE
        
        for res_id, hash in resources:
            #creator=db.execute('select resources.user from resources where resources.id=%s',[res_id]).fetchall()[0][0]
            entries=db.execute('select id,name from options where type_id=%s',[typeid]).fetchall()
            key=['#', 'UUID']
            key_id=['UUID']
            val=[count, hash]
            count=count-1
            json_col=[]
            json_col.append( dict(uuid=hash) )
            
            for opt_id, v in entries:
                try:
                    key.append(v)
                    key_id.append(opt_id)
                except:
                    key.append("")
                    key_id.append("")
                
                entries=db.execute('select value from value where res_id=%s and option_id=%s', [res_id, opt_id]).fetchall()
                try:
                    val.append(entries[0][0])
                    json_row.append( dict( uuid=hash, opt_id=opt_id, name=v, value=entries[0][0] ))
                except:
                    val.append("")
                    json_row.append( dict( uuid=hash, opt_id=opt_id, name=v, value=""))
            
            val2.append(val)
            
            json_row2.append( (json_row) )
            json_row=[]
    
    else: # Если тип не задан, отдаем пустую страницу
        return render_template( 'index.html', entries="", cols_names="", typename=typename, page=0, COUNT_PAGE=0)
        
    ### Экспорт в JSON
    if request.args.get('json') is not None:
        return simplejson.dumps(json_row2)
         
    ### Отображение таблицы на главном экране
    else:
        try:
            return render_template( 'index.html', entries=val2, cols_names=key, typename=typename, page=page, COUNT_PAGE=COUNT_PAGE)
        except:
            return render_template( 'index.html', entries="", cols_names="", typename=typename, page=0, COUNT_PAGE=0)




''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
### - - - - - Authorization - - - - - ###
''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
def loginLDAP(email, password):
    ld = ldap.open(LDAP_SERVER, LDAP_PORT)
    try:
        ld.simple_bind_s(email, password)
    except ldap.INVALID_CREDENTIALS:
        return False
    return True

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        db = get_db()
        
        reqlogin = request.form['login']
        reqpass = request.form['password']
        
        entries = db.execute('select login, password from users where login=%s limit 1', [reqlogin] ).fetchall()

        for login, user_password in entries:
            if hashlib.sha512(reqpass).hexdigest() == user_password:
                session['logged_in'] = True
                session['login']=reqlogin
                g.user=reqlogin
                flash('You were logged in')
                return redirect(url_for('index'))

        try:
            session['logged_in']
        except:
            if 'at-consulting' not in reqlogin:
                reqlogin = reqlogin+'@at-consulting.ru'
                
            if loginLDAP(reqlogin, reqpass):
                session['logged_in'] = True
                reqlogin=reqlogin.lower().replace('@at-consulting.ru','').replace('at-consulting\\','')

                session['login']=reqlogin
                flash('You were logged in')
                #return reqlogin
                return redirect(url_for('index'))
            else:
                error = "Invalid User or Password"
    
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('login', None)
    #flash('You were logged out')
    return redirect(url_for('login'))


    
# Функция выполняется при каждом запросе
@app.before_request
def before_request():
    if not session.get('logged_in') and request.endpoint != 'static' and request.endpoint != 'login': # Если пользователь не вошел в систему
        g.user=None
        flash("Need authorized")
        return render_template('login.html', error="Need authorized")
        
    else:
        g.user = session.get('login')
        
        db = get_db()
        try:
            user_exist=db.execute('SELECT login FROM users WHERE login=%s', [session['login']]).fetchall()[0][0]
        except:
            user_exist=None
            
        if user_exist is not None:
            db.execute('update users set last_activity=%s WHERE login=%s', [datetime.datetime.now(), session['login']])
        else:
            try:
                db.execute('insert into users set login=%s', [session['login']])
            except:
                pass


                
### -----------------------------------------------------------------
### Панель управления ............................................###
"""..............................................................."""

@app.route('/control/', defaults={'action': "0"})
@app.route('/control/<action>')
def control(action):
   
    db = get_db()

    type_cols = db.execute('select * from types order by id desc').fetchall()

    query = 'select * from options'
    option_cols = db.execute(query).fetchall()

    user_cols = db.execute('select id, login, full_name, email from users order by id desc').fetchall()

    type_count={}
    count = db.execute('select id from types').fetchall()
    for val in count:
        type_count[val[0]]=( db.execute('select count(id) from resources where type_id=%s', val).fetchall()[0][0] )
        
    opt_count={}
    count = db.execute('select id from options').fetchall()
    for val in count:
        opt_count[val[0]]=( db.execute('select count(id) from value where option_id=%s', val).fetchall()[0][0] )
    
    return render_template('control.html', 
        type_cols=type_cols, type_cols_names=cols_name('select * from types order by id desc'), 
        option_cols=option_cols, option_cols_names = cols_name(query),
        user_cols = user_cols, user_cols_names=cols_name('select id, login, full_name, email from users order by id desc'),
        dict_cols = db.execute('select dict_val.id as val_id, dict.id, dict.name, dict_val.value from dict, dict_val where dict.id=dict_val.dict_id order by dict.id').fetchall(), dict_cols_names=cols_name('select dict_val.id as val_id, dict.id, dict.name, dict_val.value from dict, dict_val where dict.id=dict_val.dict_id'),
        opt_count=opt_count, type_count=type_count
    )

 
app.config['UPLOAD_FOLDER'] = '/tmp/'


''' ############################### '''
###          ИМПОРТ
''' ############################### '''
@app.route('/import/<int:type_id>', methods=['GET', 'POST'])
@app.route('/import/', defaults={'type_id': 0}, methods=['GET', 'POST'])
def import_csv(type_id):
    
    db = get_db()
    
    opt_id=db.execute('select id from options where type_id=%s order by id', [type_id]).fetchall()
    opt_id_count=db.execute('select count(id) from options where type_id=%s', [type_id]).fetchall()[0][0]

    query=""
    count=0
    
    #f = request.files['file']
    #f.save('/tmp/' + secure_filename(f.filename))

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #try:
        csv_file=app.config['UPLOAD_FOLDER']+filename
        with open(csv_file, 'r') as f:
            reader = csv.reader(f, delimiter=b',',quotechar=b'"')
            for row in reader:
                res_id=addres(type_id)
                opt_id_seq=0
                for val in row:
                    if opt_id_seq >= opt_id_count: # Если число опцый в выбранном типе меньше чем в импортируемом CSV файле то добавляем новую опцию
                        db.execute('insert into options set name=%s, type_id=%s', ['IMPORT_TEMP_'+str(opt_id_seq), type_id] )
                        opt_id=db.execute('select id from options where type_id=%s order by id', [type_id]).fetchall()
                        opt_id_count=db.execute('select count(id) from options where type_id=%s', [type_id]).fetchall()[0][0]

                    query='insert into value (option_id, value, res_id) values (%s, "%s", %s)' % (opt_id[opt_id_seq][0], val, res_id)
                    db.execute( query )
                
                    opt_id_seq=opt_id_seq+1
                count=count+1
        f.close()
        
    #except:
        #flash('Ошибка в процессе парсинга файла')

    flash('Число импортированных записей: '+str(count))
    
    return redirect(url_for('control'))


@app.route('/export/<typename>')
@app.route('/export/', defaults={'typename': None})
def export_csv(typename):
    if typename is not None:
        
        try:
            res_id = engine.execute('select id from resources where type_id in (select id from types where name=%s)',[typename]).fetchall()
            opt_id = engine.execute('select id from options where type_id in (select id from types where name=%s)',[typename]).fetchall()
        except:
            flash('Некорректный тип')
            return redirect(url_for('control'))
            
        CSV=""
        
        for resid in res_id:
            count=0
            for optid in opt_id:
                count=count+1
                try:
                    CSV=CSV+'"'+engine.execute('select value from value where res_id= %s and option_id=%s',[resid[0], optid[0]]).fetchall()[0][0]+'"'
                except:
                    CSV=CSV+'""'
                if count < len(opt_id):
                    CSV=CSV+','
            CSV=CSV+'<br>'
        
        export_file_name = str("export_"+'_'+typename+'_'+str(datetime.datetime.now())+'.csv')
        f = open('exports/'+export_file_name, 'w')
        f.write(CSV)
        
        f = open('exports/'+export_file_name, 'r')
        data = f.read()
        response = make_response(data)
        response.headers["Content-Disposition"] = "attachment; filename="+export_file_name
        f.close()
        return response
        
    return redirect(url_for('control'))


''' ############################### '''
###          СТАНИЦЫ ОШИБОК
''' ############################### '''
@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


#############################################################
# DB 
#
def get_db():
    #
    #if not hasattr(g, app.config['DATABASE']):
    #    g.sqlite_db = connect_db()
    return engine

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')
    
    

#############################################
# App RUN
#
if __name__ == '__main__':
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'], port=app.config['PORT'])


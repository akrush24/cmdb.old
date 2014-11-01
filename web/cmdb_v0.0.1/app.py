#! /usr/bin/env python
# -*- coding: utf-8 -*-

# All Imports
from __future__ import unicode_literals
import os, sys, ldap, datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update, delete,   text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, and_, or_, not_
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
    cursor = engine.execute(query)
    return list( cursor.keys())

##############################################
# Decoration
#

#......................................................#
#### Обработка Типов ####
@app.route('/new_type/', methods=['POST'])
def new_type():
    try:
        engine.execute('''insert into types (name) values (%s)''', request.form['name'].upper())
    except:
        flash('Ошибка, проверьте что имена типов не совпадают')
    return redirect(url_for('control'))

@app.route('/del_type/<int:id>', methods=['GET'])
def del_type(id):
    try:
        engine.execute('delete from types where id=%s', [id])
    except:
       flash('This parameter is used!') 
        
    return redirect(url_for('control'))
    
@app.route('/clear_type/<int:id>')
def clear_type(id):
    try:
        engine.execute('delete from value where res_id in (select id from resources where type_id=%s)', [id])
        engine.execute('delete from resources where type_id=%s', [id])
        flash('Данные почищены')
    except:
       flash('This parameter is used!')
        
    return redirect(url_for('control'))
    
@app.route('/get_list_type/')
def get_list_type():
    cur = engine.execute('select * from types order by id desc')
    entries = cur.fetchall()
    json_row=[]
    for en in entries:
        json_row.append(dict(en))

    return simplejson.dumps(json_row,sort_keys=True,indent=4)

@app.route('/get_user_menu/')
def get_user_menu():
    cur = engine.execute('select id, name from types order by id desc')
    entries = cur.fetchall()
    json_row=[]
    
    for en in entries:
        value=engine.execute('select count(id) from resources where type_id=%s', [en[0]]).fetchall()[0][0]
        json_row.append(dict(en, value=value))
        
    #return en[1]
    return simplejson.dumps(json_row,sort_keys=True,indent=4)

    
    
    
    
#......................................................#
#### Обработка свойств\опций ####
@app.route('/new_option/', methods=['GET', 'POST'])
def new_option():
    test=""
    for data in request.form.keys():
        value=request.form[data]
        if data != "type_id" and data[:5] != "newid" and value != "":
            option_id = data[2:]
            cur = engine.execute('update options set name=%s where id=%s', value, option_id)
            test=test+option_id+' = '+value+'; '
            
        if data[:5] == "newid" and value != "":
            engine.execute('insert into options (name, type_id) values (%s, %s)', [value, request.form['type_id']])
            test=test+'NEWID: '+data[:5]+'='+value+'; '
    return redirect(url_for('control'))


@app.route('/del_option/<int:id>')
def del_option(id):
    try:
        engine.execute('delete from options where id=%s', [id])
    except:
       flash('This parameter is used!', 'error') 
            
    return redirect(url_for('control'))

@app.route('/edit_option/', methods=['GET', 'POST'])
def edit_option():
    opt = db_session.query(Options).filter(Options.id==request.form['id']).one()
    opt.name=request.form['name']
    opt.description=request.form['description']
    try:
        opt.dict_id=request.form['dict_id']
    except:
        pass
    opt.opttype=request.form['opttype']
    db_session.flush()

    return redirect(url_for('control'))


@app.route('/clear_option/<int:id>')
def clear_option(id):
    try:
        engine.execute('delete from value where option_id=%s', [id])
        
        flash('Данные почищены')
    except:
       flash('This parameter is used!')
        
    return redirect(url_for('control'))


@app.route('/get_list_option/', methods=['GET'])
def get_list_option():
    type_id = request.args.get('type')
    opt_id = request.args.get('opt_id')

    if type_id is not None:
        cur = engine.execute('select * from options where type_id = %s order by id desc', [type_id])
    elif opt_id is not None:
        cur = engine.execute('select * from options where id = %s order by id desc', [opt_id])
    else:
        cur = engine.execute('select * from options order by id desc')
        
    entries = cur.fetchall()
    json_row=[]
    for en in entries:
        json_row.append(dict(en))
    
    return simplejson.dumps(json_row)

    
    
    
    
#......................................................#
#### Обработка пользователей ####
@app.route('/new_user/', methods=['GET', 'POST'])
def new_user():
    engine.execute('insert into users (login, full_name, email, password) values (%s, %s, %s, %s)',
                [request.form['login'], request.form['full_name'], request.form['email'], hashlib.sha512(request.form['password']).hexdigest()]  )
    
    return redirect(url_for('control'))

@app.route('/del_user/<int:id>', methods=['GET'])
def del_user(id):
    engine.execute('delete from users where id=%s', [id])

    return redirect(url_for('control'))

@app.route('/get_list_user/', methods=['GET'])
def get_list_user():
    username = request.args.get('email_list')
    if username is not None:
        cur = engine.execute( 'select login, full_name from users WHERE upper(full_name) like upper(%s) order by id desc', username+'%' )
        #cur = engine.execute( 'select * from users WHERE upper(full_name) like upper("%'+user+'%") or upper(login) like upper("%'+user+'%") order by id desc' )
    else:
        cur = engine.execute('select login, full_name from users order by id desc limit 10')
    entries = cur.fetchall()
    json_row=[]
    for en in entries:
        json_row.append(dict(en))
    
    return simplejson.dumps(json_row)



#......................................................#
#### Обработка Словарей ####
@app.route('/new_dict/', methods=['POST'])
def new_dict():
    if request.form['name'] != "":
        try:
            engine.execute('insert into dict (name) values (%s)', request.form['name'])
            for data in request.form.keys():
                value=request.form[data]
                if data != "name" and data[:5] == "newid" and value != "":
                    engine.execute('insert into dict_val (dict_id, value) values ((select id from dict where name=%s), %s)', [request.form['name'],value])
        except:
            flash ("Ошибка при добавлении словаря")

    return redirect(url_for('control'))


@app.route('/del_dict/<int:id>')
def del_dict(id):
    engine.execute('delete from dict_val where id=%s', [id])
    return redirect(url_for('control'))

@app.route('/get_list_dict/', methods=['GET'])
def get_list_dict():
    dict_id = request.args.get('dict_id')

    if dict_id is not None:
        entries = engine.execute('select dict_val.id as val_id, dict.id, dict.name, dict_val.value from dict, dict_val where  dict.id=dict_val.dict_id and dict.id=%s', dict_id).fetchall()
    else:
        entries = engine.execute('select id, name from dict').fetchall()

    json_row=[]
    for en in entries:
        json_row.append(dict(en))
    
    return simplejson.dumps(json_row,sort_keys=True, indent=4)




#......................................................#
#### Обработка Ресурсов ####

# Удаление..............................................
@app.route('/del/<typename>/<hash>')
def del_res(hash, typename):
    engine.execute('delete from value where res_id in (SELECT id FROM resources Where hash=%s)', [hash])
    engine.execute('delete from resources where hash=%s', [hash])
    return redirect(url_for('index', typename=typename))

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Создание..............................................
def addres(type_id): # добавляем новый элемент в таблицу Resources
    UUID = id_generator(10,"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        
    ALL_HASH=engine.execute('select hash from resources').fetchall()
    hashs=[]
        
    for h in ALL_HASH:
        hashs.append(h)
        
    if UUID is not hashs:
        pass
    else:
        UUID = id_generator(6,"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        
    engine.execute('insert into resources (hash, type_id, user, create_date) values (%s, %s, %s, %s)', [UUID, type_id, session['login'], datetime.datetime.now() ])
    res_id=engine.execute('select id from resources where hash=%s limit 1', [UUID]).fetchall()[0][0]
    return res_id

@app.route('/newres', methods=['POST'])
def newres():
    try:
        typename = engine.execute('select name from types where id=%s', [request.form['type_id']]).fetchall()[0][0]
        res_id=addres(request.form['type_id'])
        
        #return str(res_id)
        for data in request.form.keys():
            if data != "type_id":
                option_id = data[2:]
                value=request.form[data]
                cur = engine.execute('insert into value (option_id, value, res_id) values (%s, %s, %s)', [option_id, value, res_id])

    except:
        flash('Unexpected ERROR')

    return redirect(url_for('index', typename=typename))


# Редактирование.............................................
@app.route('/editres', methods=['GET', 'POST'])
def editres(): 
        for data in request.form.keys():
            if data != "uuid":
                option_id = data[2:]
                value=request.form[data]
                
                option_exist=None
                try:
                    option_exist=engine.execute('select id from value where option_id=%s and res_id in (select id from resources where hash=%s)', [option_id, request.form['uuid']]).fetchall()[0][0]
                    engine.execute( 'update value SET value=%s where option_id=%s and res_id in (select id from resources where hash=%s)', [value, option_id, request.form['uuid']] )
                except IndexError:
                    engine.execute( 'insert into value (option_id, value, res_id) values (%s, %s, (select id from resources where hash=%s))', [option_id, value, request.form['uuid']] )
        try:
            typename=engine.execute('select types.name from types, resources where resources.type_id=types.id and resources.hash=%s', [request.form['uuid']]).fetchall()[0][0]
        except:
            typename=""
        return redirect(url_for('index', typename=typename)+'?hash='+request.form['uuid'])


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
        try:
            typeid=engine.execute('select id from types where name=%s',[typename]).fetchall()[0][0]
        except IndexError:
            typeid=None
            return render_template( 'index.html', entries="", cols_names="", typename=typename)

        if uuid is not None:
            resources=engine.execute('select resources.id, hash from resources where BINARY resources.hash=%s and resources.type_id=%s', [uuid, typeid]).fetchall()
            count=engine.execute('select count(id) from resources where resources.type_id=%s',[typeid]).fetchall()[0][0] # число ресурсов по выбранному типу
        elif request.args.get('save') is not None:
            resources=engine.execute('select resources.id, hash from resources where resources.type_id=%s order by id desc',[typeid]).fetchall()
            count=engine.execute('select resources.id, hash from resources where resources.type_id=%s order by id desc',[typeid]).fetchall()[0][0] # число ресурсов по выбранному типу
        else:
            ROW_IN_PAGE=50 # Число строк на одну таблицу
            COUNT_RES=engine.execute('select count(id) from resources where resources.type_id=%s',[typeid]).fetchall()[0][0] # число ресурсов по выбранному типу
            
            if COUNT_RES != 0:
                COUNT_PAGE=round(COUNT_RES/ROW_IN_PAGE+0.5, 0)
            else:
                COUNT_PAGE=0
            COUNT_PAGE=int(COUNT_PAGE)
                
            resources=engine.execute('select resources.id, hash from resources where resources.type_id=%s order by id desc LIMIT %s, %s',
            [typeid, (page-1)*ROW_IN_PAGE, ROW_IN_PAGE ] ).fetchall()

            count=COUNT_RES-(page-1)*ROW_IN_PAGE
        
        for res_id, hash in resources:
            #creator=engine.execute('select resources.user from resources where resources.id=%s',[res_id]).fetchall()[0][0]
            entries=engine.execute('select id,name from options where type_id=%s',[typeid]).fetchall()
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
                
                entries=engine.execute('select value from value where res_id=%s and option_id=%s', [res_id, opt_id]).fetchall()
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

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
### - - - - - Страничка логина - - - - - ###
''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':     
        reqlogin = request.form['login']
        reqpass = request.form['password']
        entries = engine.execute('select login, password from users where login=%s limit 1', [reqlogin] ).fetchall()
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
                return redirect(url_for('index'))
            else:
                error = "Invalid User or Password"
    
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('login', None)
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
        try:
            user_exist=engine.execute('SELECT login FROM users WHERE login=%s', [session['login']]).fetchall()[0][0]
        except:
            user_exist=None
            
        if user_exist is not None:
            engine.execute('update users set last_activity=%s WHERE login=%s', [datetime.datetime.now(), session['login']])
        else:
            try:
                engine.execute('insert into users set login=%s', [session['login']])
            except:
                pass


                
### -----------------------------------------------------------------
### Панель управления ............................................###
"""..............................................................."""

@app.route('/control/', defaults={'action': "0"})
@app.route('/control/<action>')
def control(action):
    type_cols = engine.execute('select * from types order by id desc').fetchall()
    option_cols = engine.execute('select * from options').fetchall()
    user_cols = engine.execute('select id, login, full_name, email from users order by id desc').fetchall()

    type_count={}
    count = engine.execute('select id from types').fetchall()
    for val in count:
        type_count[val[0]]=( engine.execute('select count(id) from resources where type_id=%s', val).fetchall()[0][0] )
        
    opt_count={}
    count = engine.execute('select id from options').fetchall()
    for val in count:
        opt_count[val[0]]=( engine.execute('select count(id) from value where option_id=%s', val).fetchall()[0][0] )
    
    return render_template('control.html', 
        type_cols=type_cols, type_cols_names=cols_name('select * from types order by id desc'), 
        option_cols=option_cols, option_cols_names = cols_name('select * from options'),
        user_cols = user_cols, user_cols_names=cols_name('select id, login, full_name, email from users order by id desc'),
        dict_cols = engine.execute('select dict_val.id as val_id, dict.id, dict.name, dict_val.value from dict, dict_val where dict.id=dict_val.dict_id order by dict.id').fetchall(), dict_cols_names=cols_name('select dict_val.id as val_id, dict.id, dict.name, dict_val.value from dict, dict_val where dict.id=dict_val.dict_id'),
        opt_count=opt_count, type_count=type_count
    )




''' ############################### '''
###          ИМПОРТ
''' ############################### '''
@app.route('/import/<int:type_id>', methods=['GET', 'POST'])
@app.route('/import/', defaults={'type_id': 0}, methods=['GET', 'POST'])
def import_csv(type_id):
    opt_id = db_session.query(Options.id).filter(Options.type_id==type_id)
    opt_id_count = db_session.query(Options).filter(Options.type_id==type_id).count()
    count=0
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    csv_file=app.config['UPLOAD_FOLDER']+filename
    query=""
    #try:
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=b',',quotechar=b'"')
        #reader = csv.reader(f, delimiter=b';')
        for row in reader:
            res_id=addres(type_id)
            opt_id_seq=0
            for val in row:
                if opt_id_seq >= opt_id_count: # Если число опцый в выбранном типе меньше чем в импортируемом CSV файле то добавляем новую опцию
                    # Добавляем новую опцию с временным именем
                    new_oprion_name='IMPORT_TMP#'+str(opt_id_seq)
                    new_option=Options(name=new_oprion_name, type_id=type_id)
                    db_session.add( new_option )
                    db_session.commit()
                    
                    opt_id = db_session.query(Options.id).filter(Options.type_id==type_id)
                    opt_id_count = db_session.query(Options).filter(Options.type_id==type_id).count()

                db_session.add( Value(option_id=opt_id[opt_id_seq][0], value=val, res_id=res_id) )
                opt_id_seq=opt_id_seq+1
            count=count+1
        f.close() 
    #except:
    #    flash('Ошибка в процессе парсинга файла: '+query)
        
    flash('Число импортированных записей: '+str(count))
    return redirect(url_for('control'))


''' ############################### '''
###          EXPORT
''' ############################### '''
@app.route('/export/<typename>')
@app.route('/export/', defaults={'typename': None})
def export_csv(typename):
    if typename is not None:
        try:
            res_id = db_session.query(Resources.id).filter(Resources.type_id==db_session.query(Types.id).filter(Types.name==typename))
            opt_id = db_session.query(Options.id).filter(Options.type_id==db_session.query(Types.id).filter(Types.name==typename))
        except:
            flash('Некорректный тип')
            return redirect(url_for('control'))
        CSV=""
        for resid in res_id:
            count=0
            for optid in opt_id:
                count=count+1
                try:
                    CSV=CSV+'"'+db_session.query(Value.value).filter(Value.res_id==resid[0], Value.option_id==optid[0])[0][0]
                except:
                    CSV=CSV+'""'
                if count < opt_id.count():
                    CSV=CSV+','
                else:
                    CSV=CSV+"\n"
        
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
###          EXPORT JSON
''' ############################### '''
@app.route('/export_json/')
def export_json():
    json_row=[]
    json_row2=[]

    if request.args.get('uuid') is not None:
        uuid = request.args.get('uuid')
        if uuid is not None:
            resources=engine.execute('select resources.id, hash from resources where BINARY resources.hash=%s', [uuid]).fetchall()

        for res_id, hash in resources:
            entries=engine.execute('select id, name, opttype, dict_id from options where type_id in (select type_id from resources where hash=%s)',[uuid]).fetchall()

            for opt_id, v, opttype, dict_id in entries:
                    
                entries=engine.execute('select value from value where res_id=%s and option_id=%s order by value', [res_id, opt_id]).fetchall()
                try:
                    json_row.append( dict( uuid=hash, opt_id=opt_id, name=v, opttype=opttype, dict_id=dict_id, value=entries[0][0] ))
                except:
                    json_row.append( dict( uuid=hash, opt_id=opt_id, name=v, opttype=opttype, dict_id=dict_id, value=""))
            
            json_row2.append( (json_row) )
            json_row=[]
            
            return simplejson.dumps(json_row2)
    
    else: # Если uuid задан, отдаем пустую страницу
        return render_template( 'index.html', entries="", cols_names="", typename="", page=0, COUNT_PAGE=0)



''' ##############################################'''
################# Функция поиска ###################
@app.route('/search', methods=['GET'])
def search():
    str = request.args.get('term')
    if str != "":     
        JSON=[]
        for value in engine.execute( '''select types.name as type, value.value, options.name as opt, resources.hash from types, resources, value, options where value like %s and value.option_id=options.id and value.res_id=resources.id and types.id=resources.type_id LIMIT 15''', ['%'+str+'%'] ).fetchall():
            JSON.append(dict(value))
        return simplejson.dumps(JSON,sort_keys=True,indent=4)
    return redirect(url_for('index'))



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

''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
### Отрабатывает после окончания каждого запроса ###
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.commit()
    db_session.remove()


#######################################################
''' FOR TESTING '''
#######################################################
@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')

@app.route('/s/')
def s():
    # SELECT
    '''
    s = select( [Users], and_(Users.login.like('a%'), Users.id<999) ).order_by(Users.id.desc())
    result = engine.execute(s)
    return str(result.fetchall())
    '''
    
    #INSERT
    db_session.add(Users(login='test299'))
    return "OK"
    
    
    
    

#############################################
# App RUN
#
if __name__ == '__main__':
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'], port=app.config['PORT'])


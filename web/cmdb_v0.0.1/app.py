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

''' Добавление нового типа '''
@app.route('/new_type/', methods=['POST'])
def new_type():
    try:
        type_name=request.form['name'].upper()
        new = Types( name=request.form['name'].upper() )
        db_session.add( new )
        db_session.commit()
        
        types=db_session.query(Types.id).filter(Types.name==request.form['name'].upper()).one()
        type_id=types.id
        
        db_session.add( Score( type_id=type_id, score=0 ) ) # добавляем счетчик Итемов, начинается с 0
    except Exception as e: 
        flash('Ошибка, проверьте что имена типов:'+request.form['name'].upper()+' не совпадают. \n '+str(e) )
        return redirect(url_for('control'))
    
    try:
        sort=0
        for option_id in request.values.getlist('options'):
            new=Relation( type_id=type_id, option_id=option_id, sort=sort )
            sort=sort+1
            db_session.add( new )
    except Exception as e:
        flash('Ошибка добавления опций к типу:'+request.form['name'].upper())
        flash(str(e))
    
    return redirect(url_for('control'))

''' Удаление типа '''
@app.route('/del_type/<int:id>', methods=['GET'])
def del_type(id):
    try:
        engine.execute('delete from types where id=%s', [id])
        engine.execute('delete from score where type_id=%s', [id])
        engine.execute('delete from relation where type_id=%s', [id])
    except:
       flash('This parameter is used!') 
        
    return redirect(url_for('control'))
    
@app.route('/clear_type/<int:id>')
def clear_type(id):
    try:
        engine.execute('delete from value where res_id in (select id from items where type_id=%s)', [id])
        engine.execute('delete from items where type_id=%s', [id])
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

# по данному JSON стоится выпадающая меню "Мои ресурсы"
@app.route('/get_user_menu/')
def get_user_menu():
    cur = engine.execute('select id, name from types order by id desc')
    entries = cur.fetchall()
    json_row=[]
    
    for en in entries:
        value=engine.execute('select count(id) from items where type_id=%s', [en[0]]).fetchall()[0][0]
        json_row.append(dict(en, value=value))
        
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
    try: # поле request.form['dict_id'] приходит не во всех случаях, поэтому специально инициализируем эту переменную
        dict_id=request.form['dict_id']
    except:
        dict_id=None
        
    try:
        description = request.form['description']
    except:
        description = None
        
    try:
        name = request.form['name']
    except:
        name = None
        
    if request.form['id'] == 'new':
        new_option=Options(name=request.form['name'],description=description,user_visible=request.form['user_visible'],front_page_visible=request.form['front_page_visible'],required=request.form['required'],option_type=request.form['option_type'], dict_id=dict_id )
        db_session.add( new_option )
    else:
        opt = db_session.query(Options).filter(Options.id==request.form['id']).one()
        opt.name=name
        opt.description=description
        opt.user_visible=request.form['user_visible']
        opt.front_page_visible=request.form['front_page_visible']
        opt.required=request.form['required']
        opt.dict_id=dict_id
        opt.option_type=request.form['option_type']
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
        cur = engine.execute('select * from options where id in (select option_id from relation where type_id=%s order by sort)', [type_id])
        cur = engine.execute('select options.* from relation, options where relation.type_id=%s and options.id=relation.option_id order by relation.sort', [type_id])
        
    elif opt_id is not None:
        if opt_id=='new':
            return '[{"name": "", "front_page_visible": "0", "description": "", "required": "0", "option_type": "input", "user_visible": "1", "dict_id": ""}]'
        else:
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

@app.route('/get_list_user_ldap/', methods=['GET'])
def get_list_user_ldap():
    username = request.args.get('term')
    
    ad = ldap.initialize("ldap://192.168.10.2")
    ad.protocol_version = ldap.VERSION3
    ad.set_option(ldap.OPT_REFERRALS, 0)
    ad.simple_bind_s('vmtest', 'qwerty$4')

    basedn = 'DC=at-consulting,DC=ru'
    scope = ldap.SCOPE_SUBTREE
    #attrlist = ["sAMAccountName", "mail"]
    attrlist = [b'cn', b"mail", b"sAMAccountName", b"title", b"telephoneNumber"]
    
    if username:
        filterexp = "(&(objectCategory=Person)(sAMAccountName=*)(cn=*%s*))" % username
        results = ad.search_s(basedn, scope, filterexp, attrlist)

        filterexp = "(&(objectCategory=Person)(sAMAccountName=*%s*)(cn=*))" % username
        results = results+ad.search_s(basedn, scope, filterexp, attrlist)        

    ldap_users=[]
    count=1
    for result in results:
        if count <20:
            try:
                result[1]["mail"][0]
                try:
                    JobTitle=result[1]["title"][0]
                except:
                    JobTitle="NONE"
                try:
                    telephoneNumber=result[1]["telephoneNumber"][0]
                except:
                    telephoneNumber="NONE"                    
                ldap_users.append(dict(login=result[1]["sAMAccountName"][0], email=result[1]["mail"][0], fio=result[1]["cn"][0], jobtitle=JobTitle, telephoneNumber=telephoneNumber))
            except: #If No MAIL...
                pass
        count=count+1
        
    return simplejson.dumps(ldap_users)



#......................................................#
#### Обработка Словарей ####
@app.route('/new_dict/', methods=['POST'])
def new_dict():
    if request.form['name'] != "":
        try:
            engine.execute('insert into dict_s (name) values (%s)', request.form['name'])
            for data in request.form.keys():
                value=request.form[data]
                if data != "name" and data[:5] == "newid" and value != "":
                    engine.execute('insert into dict (dict_id, value) values ((select id from dict_s where name=%s), %s)', [request.form['name'],value])
        except:
            flash ("Ошибка при добавлении словаря")

    return redirect(url_for('control'))


@app.route('/del_dict/<int:id>')
def del_dict(id):
    engine.execute('delete from dict where id=%s', [id])
    return redirect(url_for('control'))

@app.route('/get_list_dict/', methods=['GET'])
def get_list_dict():
    dict_id = request.args.get('dict_id')

    if dict_id is not None:
        entries = engine.execute('select dict.id as val_id, dict_s.id, dict_s.name, dict.value from dict_s, dict where  dict_s.id=dict.dict_id and dict_s.id=%s', dict_id).fetchall()
    else:
        entries = engine.execute('select id, name from dict_s').fetchall()

    json_row=[]
    for en in entries:
        json_row.append(dict(en))
    
    return simplejson.dumps(json_row,sort_keys=True, indent=4)


@app.route('/del_dict_s/<int:id>')
def del_dict_s(id):
    try:
        engine.execute('delete from dict_s where id=%s', [id])
    except:
        flash('Схема используется')
    return redirect(url_for('control'))

    
    
#......................................................#
#### Обработка Ресурсов ####

# Удаление..............................................
@app.route('/del/<itemid>')
def del_res(itemid):
    r = re.findall(r"(^.+)-([\d]+)", itemid)
    id=r[0][1]
    typename=r[0][0]

    engine.execute('delete from value where res_id in (SELECT id FROM items Where hash=%s and type_id in (select id from types where name=%s))', [id, typename])
    engine.execute('delete from items where hash=%s and type_id in (select id from types where name=%s)', [id, typename])
    return redirect(url_for('index', typename=typename))

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Создание..............................................
def addres(type_id): # добавляем новый элемент в таблицу items
    score = db_session.query(Score).filter(Score.type_id==type_id).one()
    # увеличиваем количество итемов по данному ресурсы +1
    score.score = score.score+1
    db_session.flush()
    
    engine.execute('insert into items (hash, type_id, user, create_date) values (%s, %s, %s, %s)', [score.score, type_id, session['login'], datetime.datetime.now() ])
    res_id=engine.execute('select id from items where hash=%s limit 1', [score.score]).fetchall()[0][0]

    return res_id



### Добавление нового Итема
@app.route('/new_item', methods=['POST'])
def new_item():
    res_id=addres(request.form['type_id'])
    
    try:
        typename = engine.execute('select name from types where id=%s', [request.form['type_id']]).fetchall()[0][0]
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
        r = re.findall(r"(^.+)-([\d]+)", request.form['id'])
        id=r[0][1]
        types = db_session.query(Types).filter(Types.name==r[0][0]).one()
            
        for data in request.form.keys():

            if data != "id":
                option_id = data[2:]
                value=request.form[data]
                
                option_exist=None
                try:
                    option_exist=engine.execute('select id from value where option_id=%s and res_id in (select id from items where hash=%s and type_id=%s)', [option_id, id, types.id]).fetchall()[0][0]
                    engine.execute( 'update value SET value=%s where option_id=%s and res_id in (select id from items where hash=%s and type_id=%s)', [value, option_id, id, types.id] )
                except IndexError:
                    engine.execute( 'insert into value (option_id, value, res_id) values (%s, %s, (select id from items where hash=%s and type_id=%s))', [option_id, value, id, types.id] )
        try:
            typename=engine.execute('select types.name from types, items where items.type_id=types.id and items.hash=%s and items.type_id=%s', [id, types.id]).fetchall()[0][0]
        except:
            typename=""
        return redirect(url_for('index', typename=typename)+'?id='+request.form['id'])


# ..........................................................................
##### Главная страница .................................................####
@app.route('/browse/', defaults={'typename': None, 'page': 1})
@app.route('/browse/<typename>/<int:page>/')
@app.route('/browse/<typename>/', defaults={'page': 1})
@app.route('/', defaults={'typename': None, 'page': 1})
def index(typename, page):
    val2=[]
    key=[]
    
    try: # если передается переменная id (прим: ?id=SERVER-2) то по ней вычисляется имя Типа
        request.args.get('id')
        r = re.findall(r"(^.+)-([\d]+)", request.args.get('id'))
        id=r[0][1]
        typename = r[0][0]
    except:
        pass
    
    if typename is not None:
        uuid = request.args.get('uuid')
        try:
            typeid=engine.execute('select id from types where name=%s',[typename]).fetchall()[0][0]
        except IndexError:
            typeid=None
            return render_template( 'index.html', entries="", cols_names="", typename=typename)

        if uuid is not None:
            items=engine.execute('select items.id, hash from items where BINARY items.hash=%s and items.type_id=%s', [uuid, typeid]).fetchall()
            count=engine.execute('select count(id) from items where items.type_id=%s',[typeid]).fetchall()[0][0] # число ресурсов по выбранному типу
        else:
            ROW_IN_PAGE=50 # Число строк на одну таблицу
            COUNT_RES=engine.execute('select count(id) from items where items.type_id=%s',[typeid]).fetchall()[0][0] # число ресурсов по выбранному типу
            
            if COUNT_RES != 0:
                COUNT_PAGE=round(COUNT_RES/ROW_IN_PAGE+0.5, 0)
            else:
                COUNT_PAGE=0
            COUNT_PAGE=int(COUNT_PAGE)
                
            items=engine.execute('select items.id, hash from items where items.type_id=%s order by id desc LIMIT %s, %s',
            [typeid, (page-1)*ROW_IN_PAGE, ROW_IN_PAGE ] ).fetchall()

            count=COUNT_RES-(page-1)*ROW_IN_PAGE
        
        for res_id, hash in items:
            #creator=engine.execute('select items.user from items where items.id=%s',[res_id]).fetchall()[0][0]
            #entries=engine.execute('select id, name from options where type_id=%s and front_page_visible=1',[typeid]).fetchall()
            entries=engine.execute('select option_id, options.name as option_name from relation, options where relation.type_id=%s and options.id=relation.option_id and options.front_page_visible=1 order by relation.sort',[typeid]).fetchall()
            key=['Код']
            key_id=['UUID']
            g=typename+'-'+str(hash)
            val=[g]
            count=count-1
            
            for opt_id, option_name in entries:
                try:
                    key.append(option_name)
                    key_id.append(opt_id)
                except:
                    key.append("")
                    key_id.append("")
                
                entries=engine.execute('select value from value where res_id=%s and option_id=%s', [res_id, opt_id]).fetchall()
                try:
                    val.append(entries[0][0])
                except:
                    val.append("")
            
            val2.append(val)
        
        if key==[]:
            keys = db_session.query(Options.name, Relation.option_id).filter(Relation.type_id==typeid).filter(Options.id==Relation.option_id)
            key=['Код']
            for k,v in keys:
                key.append(k)
        
    else: # Если тип не задан, отдаем пустую страницу
        return render_template( 'index.html', entries="", cols_names="", page=0, COUNT_PAGE=0 )
         
    ### Отображение таблицы на главном экране

        
    return render_template( 'index.html', entries=val2, cols_names=key, typename=typename, type_id=typeid, page=page, COUNT_PAGE=COUNT_PAGE)



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
        type_count[val[0]]=( engine.execute('select count(id) from items where type_id=%s', val).fetchall()[0][0] )
        
    opt_count={}
    count = engine.execute('select id from options').fetchall()
    for val in count:
        opt_count[val[0]]=( engine.execute('select count(id) from value where option_id=%s', val).fetchall()[0][0] )
    
    return render_template('control.html', 
        type_cols=type_cols, type_cols_names=cols_name('select * from types order by id desc'), 
        option_cols=option_cols, option_cols_names = cols_name('select * from options'),
        user_cols = user_cols, user_cols_names=cols_name('select id, login, full_name, email from users order by id desc'),
        dict_cols = engine.execute('select dict.id as val_id, dict_s.id, dict_s.name, dict.value from dict_s, dict where dict_s.id=dict.dict_id order by dict_s.id').fetchall(), dict_cols_names=cols_name('select dict.id as val_id, dict_s.id, dict_s.name, dict.value from dict_s, dict where dict_s.id=dict.dict_id'),
        dict_s=engine.execute('select * from dict_s').fetchall(), dict_s_cols_names=cols_name('select * from dict_s'),
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
    try:
        with open(csv_file, 'r') as f:
            #reader = csv.reader(f, delimiter=b',',quotechar=b'"')
            reader = csv.reader(f, delimiter=b';')
            
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
    except:
        flash('Ошибка в процессе парсинга файла: '+query)
        
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
            res_id = db_session.query(items.id).filter(items.type_id==db_session.query(Types.id).filter(Types.name==typename))
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

    if request.args.get('id') is not None:
        r = re.findall(r"(^.+)-([\d]+)", request.args.get('id'))
        typename = r[0][0]
        id=r[0][1]
        
        types = db_session.query(Types).filter(Types.name==typename).one()
        
        if id is not None and types.id is not None:
            items=engine.execute('select items.id, hash, type_id from items where BINARY items.hash=%s and type_id=%s', [id, types.id]).fetchall()

        for res_id, hash, type_id in items:
            entries=engine.execute('select option_id, options.name as option_name, option_type, dict_id from relation, options where relation.type_id=%s and options.id=relation.option_id',[types.id]).fetchall()

            for option_id, option_name, option_type, dict_id in entries:
                entries=engine.execute('select value from value where res_id=%s and option_id=%s order by value', [res_id, option_id]).fetchall()
                try:
                    json_row.append( dict( id=hash, opt_id=option_id, name=option_name, option_type=option_type, dict_id=dict_id, type_id=type_id, value=entries[0][0] ))
                except:
                    json_row.append( dict( id=hash, opt_id=option_id, name=option_name, option_type=option_type, dict_id=dict_id, type_id=type_id, value="" ))
            json_row2.append( (json_row) )
            json_row=[]

            return simplejson.dumps(json_row2)
    else: # Если id задан, отдаем пустую страницу
        return render_template( 'index.html', entries="", cols_names="", typename="", page=0, COUNT_PAGE=0)



''' ##############################################'''
################# Функция поиска ###################
@app.route('/search', methods=['GET'])
def search():
    str = request.args.get('term')
    if str != "":     
        JSON=[]
        for value in engine.execute( '''select types.name as type, value.value, options.name as opt, items.hash from types, items, value, options where value like %s and value.option_id=options.id and value.res_id=items.id and types.id=items.type_id LIMIT 15''', ['%'+str+'%'] ).fetchall():        
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


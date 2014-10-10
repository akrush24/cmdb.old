#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
import mysql.connector
import calendar, datetime
import os
import Cookie

# Устанавливаем подключение к БД
mydb=mysql.connector.connect(user='cmdb',password='unix11',host='cmdb.at-consulting.ru',database='cmdb')
cursor=mydb.cursor()

# Получение значений, введенных пользователем
GET = cgi.FieldStorage()
if 'user' in GET:
	user = GET["user"].value
if 'password' in GET:
	password = GET["password"].value

cookie = Cookie.SimpleCookie()

cookie['HASH']="123"
cookie['HASH']['expires']=1*1*3*60*60	

print "Content-Type: text/html;charset=utf-8"
print ""
		
try:
	user, password
except NameError:
	print "Content-Type: text/html;charset=utf-8"
	print ""
	
	# The returned cookie is available in the os.environ dictionary
	cookie_string = os.environ.get('HTTP_COOKIE')

	# The first time the page is run there will be no cookies
	if not cookie_string:
		print '<p>First visit or cookies disabled</p>'
	else: # Run the page twice to retrieve the cookie
		#print '<p>The returned cookie string was "' + cookie_string + '"</p>'
		cookie.load(cookie_string)
		hash = cookie['HASH'].value
		query='SELECT `id`,`login`,`pass`,`cookie` FROM `users` WHERE cookie="'+hash+'"'
		cursor.execute(query)
		rows = cursor.fetchall()
		for row in rows:
			db_user_id, db_user_login, db_user_pass, db_user_cookie  = row

			if db_user_cookie == hash:
				print "USER: %s, Authentication Ok!" % db_user_login
			else:
				print "You need Authentication"
   
else:

	query='SELECT `id`,`login`,`pass`,`cookie` FROM `users` WHERE login="'+user+'"'
	cursor.execute(query)
	rows = cursor.fetchall()
	for row in rows:
		db_user_id, db_user_login, db_user_pass, db_user_cookie  = row

	if user == db_user_login and password == db_user_pass:
		hash = os.urandom(16).encode('hex')


		
		cursor.execute("UPDATE `cmdb`.`users` SET  `cookie` =  '%s' WHERE `login`='%s';" % (hash, user))
		mydb.commit();		


		
		print "Content-Type: text/html;charset=utf-8"
		print ""
		
		print 'Set-Cookie: HASH=%s' % hash;
		
	else:
		print "Authentication Failed!"
	

# Разрываем подключение с БД
mydb.close()
	




print "EOF"
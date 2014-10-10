#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
import mysql.connector
import calendar, datetime
import os
 
print "Content-Type: text/html;charset=utf-8"
print ""

# Получение значений, введенных пользователем
GET = cgi.FieldStorage()
if 'user' in GET:
	user = GET["user"].value
if 'password' in GET:
	password = GET["password"].value

 
try:
	user, password
except NameError:
  print "user or password not defined!"
else:
	
	mydb=mysql.connector.connect(user='cmdb',password='unix11',host='cmdb.at-consulting.ru',database='cmdb')
	cursor=mydb.cursor()
	
	query='SELECT `id`,`login`,`pass`,`cookie` FROM `users` WHERE login="'+user+'"'
	cursor.execute(query)
	rows = cursor.fetchall()
	for row in rows:
		db_user_id, db_user_login, db_user_pass, db_user_cookie  = row

	if user == db_user_login and password == db_user_pass:
		hash = os.urandom(16).encode('hex')

		cursor.execute("UPDATE `cmdb`.`users` SET  `cookie` =  '%s' WHERE `login`='%s';" % (hash, user))
		mydb.commit();
	
	else:
		print "Authentication Failed!"
	

	mydb.close()
	

#print " "
print "EOF"
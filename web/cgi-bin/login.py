#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
import mysql.connector
import calendar, datetime
import hashlib
 
print "Content-Type: text/html;charset=utf-8"
print ""

GET = cgi.FieldStorage()
if 'user' in GET:
	user = GET["user"].value
if 'password' in GET:
	password = GET["password"].value

#user="admin"

mydb=mysql.connector.connect(user='cmdb',password='unix11',host='cmdb.at-consulting.ru',database='cmdb')
cursor=mydb.cursor()
query='SELECT `id`,`login`,`pass`,`cookie` FROM `users` WHERE login="'+user+'"'

cursor.execute(query)
rows = cursor.fetchall()
#print rows

for row in rows:
	db_user_id, db_user_login, db_user_pass, db_user_cookie  = row

mydb.close()

h = hashlib.new('ripemd160')
h.update("Nobody inspects the spammish repetition")
h.hexdigest()

if user == db_user_login and password == db_user_pass:
	print "OK"
	print h
else:
	print "0"


#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi
import urllib
import urllib2

print "Content-Type: text/html;charset=utf-8"
print ""

GET = cgi.FieldStorage()

if 'user' in GET:
	user = GET["user"].value
if 'password' in GET:
	password = GET["password"].value

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

if user == "vk@at-consulting.ru" and password == "qwerty":
	#print "1"
	html = urllib.urlopen('http://google.com').read()
	print html
else:
	print "0"
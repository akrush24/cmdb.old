#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import cgi
import urllib
import urllib2
import Cookie


# create the cookie
c=Cookie.SimpleCookie()
# assign a value
c['cmdb.at-consulting.ru']='Hello world'
# set the xpires time
c['cmdb.at-consulting.ru']['expires']=1*1*3*60*60

# print the header, starting with the cookie
print c
print "Content-Type: text/html;charset=utf-8"
print ""

# empty lines so that the browser knows that the header is over
print ""
print ""

# now we can send the page content
print """
<html>
    <body>
        <h1>The cookie has been set</h1>
    </body>
</html>
"""
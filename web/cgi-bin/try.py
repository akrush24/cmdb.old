#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import cgi
import urllib
import urllib2
import Cookie
import time

# Instantiate a SimpleCookie object
cookie = Cookie.SimpleCookie()

# The SimpleCookie instance is a mapping
cookie['lastvisit'] = str(time.time())

# Output the HTTP message containing the cookie
print cookie
print "Content-Type: text/html;charset=utf-8"
print ""

print '<html><body>'
print 'Server time is', time.asctime(time.localtime())
print '</body></html>'
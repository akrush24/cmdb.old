#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import cgi
import urllib
import urllib2
import Cookie

print "Content-Type: text/html;charset=utf-8"
print ""

print """
<html>
<body>
<h1>Check the cookie</h1>
"""

if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=Cookie.SimpleCookie()
    c.load(cookie_string)

    try:
        data=c['cmdb'].value
        print "cookie data: "+data+"<br>"
    except KeyError:
        print "The cookie was not set or has expired<br>"


print """
</body>
</html>

"""
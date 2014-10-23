#!/usr/bin/env python

import ldap, sys

server = 'ldap://192.168.10.8'
l = ldap.initialize(server)
try:
    l.start_tls_s()
except ldap.LDAPError, e:
    print e.message['info']
    if type(e.message) == dict and e.message.has_key('desc'):
        print e.message['desc']
    else:
        print e
    sys.exit()

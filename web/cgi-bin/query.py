#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()
import mysql.connector

print "Content-Type: text/plain;charset=utf-8"
print

cnx=mysql.connector.connect(user='cmdb',password='unix11',host='cmdb.at-consulting.ru',database='cmdb')
cursor=cnx.cursor()
query=('select cmdb.properties.prop_name, cmdb.values.value, cmdb.types.type_name, cmdb.values.up_date from cmdb.resources, cmdb.types, cmdb.properties, cmdb.values where cmdb.values.uuid = cmdb.resources.uuid and cmdb.types.type_id = cmdb.resources.type_id and cmdb.properties.prop_id = cmdb.values.prop_id and cmdb.values.last_value = 1')
cursor.execute(query)
for row in cursor:
    print row

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import mysql.connector
import MySQLdb

print "Content-Type: text/plain;charset=utf-8"
print 

mydb=MySQLdb.connect(user='cmdb',passwd='unix11',host='cmdb.at-consulting.ru',db='cmdb')
cursor=mydb .cursor()
query=('select properties.prop_name, values.value from cmdb.resources, cmdb.types, cmdb.properties, cmdb.values where cmdb.values.uuid = cmdb.resources.uuid and cmdb.types.type_id = cmdb.resources.type_id and cmdb.properties.prop_id = cmdb.values.prop_id and cmdb.values.last_value = 1')
#query=('select properties.prop_name, values.value, types.type_name, values.up_date from cmdb.resources, cmdb.types, cmdb.properties, cmdb.values where cmdb.values.uuid = cmdb.resources.uuid and cmdb.types.type_id = cmdb.resources.type_id and cmdb.properties.prop_id = cmdb.values.prop_id and cmdb.values.last_value = 1')
cursor.execute(query)
rows = cursor.fetchall()

print json.dumps(rows, indent=2)
mydb.close()

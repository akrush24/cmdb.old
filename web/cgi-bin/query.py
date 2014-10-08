#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import mysql.connector
import MySQLdb

import calendar, datetime

def default(obj):
    """Default JSON serializer."""

    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
    millis = int(
        calendar.timegm(obj.timetuple()) * 1 +
        obj.microsecond / 1000
    )
    return datetime.datetime.fromtimestamp( millis ).strftime('%Y-%m-%d %H:%M:%S')

print "Content-Type: text/plain;charset=utf-8"
print 

mydb=MySQLdb.connect(user='cmdb',passwd='unix11',host='cmdb.at-consulting.ru',db='cmdb')
cursor=mydb .cursor()
cursor.execute('select properties.prop_name, values.value, types.type_name, values.up_date from cmdb.resources, cmdb.types, cmdb.properties, cmdb.values where cmdb.values.uuid = cmdb.resources.uuid and cmdb.types.type_id = cmdb.resources.type_id and cmdb.properties.prop_id = cmdb.values.prop_id and cmdb.values.last_value = 1')
rows = cursor.fetchall()
print json.dumps(rows, indent=2, default=default)
mydb.close()

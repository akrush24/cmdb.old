#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import mysql.connector
import cgi

import calendar, datetime

## Функия для преобразования времени формата datetime.datetime(2014, 10, 8, 8, 22, 23) -> 2014-10-08 12:22:23
def time_correct(obj):
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
print ""

form = cgi.FieldStorage()
print form

# Select ALL
mydb=mysql.connector.connect(user='cmdb',password='unix11',host='cmdb.at-consulting.ru',database='cmdb')

cursor=mydb .cursor()
query='select resources.uuid, properties.prop_name, values.value, types.type_name, values.up_date from cmdb.resources, cmdb.types, cmdb.properties, cmdb.values where cmdb.values.uuid = cmdb.resources.uuid and cmdb.types.type_id = cmdb.resources.type_id and cmdb.properties.prop_id = cmdb.values.prop_id and cmdb.values.last_value = 1'
cursor.execute(query)
rows = cursor.fetchall()

mydb.close()

print json.dumps(rows, indent=2, default=time_correct)


#python
# http://webonrails.ru/post/490/
import mysql.connector

cnx=mysql.connector.connect(user='cmdb',password='unix11',host='cmdb.at-consulting.ru',database='cmdb')
cursor=cnx.cursor()
query=('select cmdb.properties.prop_name, cmdb.values.value, cmdb.type.type_name from cmdb.items, cmdb.type, cmdb.properties, cmdb.values where cmdb.values.uuid = cmdb.items.uuid and cmdb.type.type_id = cmdb.items.type_id and cmdb.properties.prop_id = cmdb.values.prop_id')
cursor.execute(query)
for row in cursor:
    print row


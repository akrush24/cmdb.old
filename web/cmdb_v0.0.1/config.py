import os
basedir = os.path.abspath(os.path.dirname(__file__))



SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

DEBUG = True
SECRET_KEY = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT$WERWER'
HOST='0.0.0.0'
PORT=5000

MYSQL_DATABASE_USER = 'cmdb'
MYSQL_DATABASE_PASSWORD = 'unix11'
MYSQL_DATABASE_DB = 'cmdb'
MYSQL_DATABASE_HOST = 'localhost'

SQLALCHEMY_DATABASE_URI = 'mysql://'+MYSQL_DATABASE_USER+':'+MYSQL_DATABASE_PASSWORD+'@'+MYSQL_DATABASE_HOST+'/'+MYSQL_DATABASE_DB+'?charset=utf8&use_unicode=0'
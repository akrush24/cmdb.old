import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://cmdb:unix11@localhost/cmdb_v.0.0.2?charset=utf8&use_unicode=0'

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'cmdb.sqlite')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

DATABASE = os.path.join(basedir, 'cmdb.sqlite')
DEBUG = True
SECRET_KEY = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
USERNAME = 'admin'
PASSWORD = 'default'
HOST='0.0.0.0'


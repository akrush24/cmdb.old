#!/home/cmdb/web/flask/bin/python
import os
import sys
import site

sys.path.insert(0, '/home/cmdb/web/cmdb_v0.0.1/')
site.addsitedir('/home/cmdb/web/flask/lib')

activate_this = '/home/cmdb/web/flask/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from app import app as application

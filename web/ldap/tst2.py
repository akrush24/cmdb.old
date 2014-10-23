from flask import Flask
from flask.ext.simpleldap import LDAP

app = Flask(__name__)
ldap = LDAP(app)

app.config['LDAP_BASE_DN'] = 'dc=at-consulting,dc=ru'
app.config['LDAP_USERNAME'] = 'OU=vmtest,DC=at-consulting,DC=ru'
app.config['LDAP_PASSWORD'] = 'qwerty$4'

LDAP_USERNAME = 'OU=vmtest,DC=at-consulting,DC=ru'

def ldap_protected():
    return 'Success!'

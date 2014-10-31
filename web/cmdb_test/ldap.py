from flask import Flask
from flask.ext.simpleldap import LDAP

app = Flask(__name__)
ldap = LDAP(app)

app.config['LDAP_BASE_DN'] = 'dc=at-consulting,dc=ru'
app.config['LDAP_USERNAME'] = 'CN=vmtest,DC=at-consulting,DC=ru'
app.config['LDAP_PASSWORD'] = 'qwerty$4'

@app.route('/ldap')
@ldap.login_required
def ldap_protected():
    return 'Success!'

app.run(host='0.0.0.0')

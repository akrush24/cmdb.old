

from flask import Flask
from flask.ext.ldap import LDAP, login_required
from flask.ext.pymongo import PyMongo
app = Flask(__name__)
app.debug = True



ldap = LDAP(app)

ldap = LDAP(app, mongo)
app.secret_key = "qwerty$4"
app.add_url_rule('/login', 'login', ldap.login, methods=['GET', 'POST'])

# coding=utf-8

from flask import Flask
from flask.ext.ldap import LDAP
app = Flask(__name__)
app.debug = True

app.config['LDAP_HOST'] = 'at-consulting.ru'
app.config['LDAP_DOMAIN'] = 'at-consulting.ru'
app.config['LDAP_SEARCH_BASE'] = 'OU=DIT,DC=at-consulting,DC=ru'
app.config['LDAP_LOGIN_VIEW'] = 'vmtest'

app.config['LDAP_AUTH_TEMPLATE'] = 'login.html'
app.config['LDAP_PROFILE_KEY'] = 'employeeID'
# app.config['LDAP_AUTH_VIEW'] = 'login'

ldap = LDAP(app)
app.secret_key = "welfhwdlhwdlfhwelfhwlehfwlehfelwehflwefwlehflwefhlwefhlewjfhwelfjhweflhweflhwel"
app.add_url_rule('/login', 'login', ldap.login, methods=['GET', 'POST'])

@app.route('/')
@ldap.login_required
def index():
        pass


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     pass

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
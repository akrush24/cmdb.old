from flask import Flask
from flask.ext.ldap import LDAP, login_required
app = Flask(__name__)
app.debug = True

app.config['LDAP_HOST'] = 'at-consulting.ru'
app.config['LDAP_DOMAIN'] = 'at-consulting.ru'
app.config['LDAP_SEARCH_BASE'] = 'DC=at-consulting.ru,DC=ru'
app.config['LDAP_LOGIN_VIEW'] = 'vmtest'

ldap = LDAP(app)
app.secret_key = "welfhwdlhwdlfhwelfhwlehfwlehfelwehflwefwlehflwefhlwefhlewjfhwelfjhweflhweflhwel"
app.add_url_rule('/login', 'login', ldap.login, methods=['GET', 'POST'])

@app.route('/')
def index():
    return ldap.login

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4000)

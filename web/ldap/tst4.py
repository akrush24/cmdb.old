LDAP_SERVER = "192.168.10.2"
LDAP_PORT = 389 # your port
import ldap
def login(email, password):
    ld = ldap.open(LDAP_SERVER, port=LDAP_PORT)
    try:
        ld.simple_bind_s(email, password)
    except ldap.INVALID_CREDENTIALS:
        return False
    return True

login ('vmtest', 'qwerty$4')

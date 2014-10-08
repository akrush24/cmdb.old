import ldap

def check_credentials(username, password):
   """Verifies credentials for username and password.
   Returns None on success or a string describing the error on failure
   # Adapt to your needs
   """
   LDAP_SERVER = 'ldap://192.168.10.2'
   # fully qualified AD user name
   LDAP_USERNAME = 'vmtest@at-consulting.ru' % username
   # your password
   LDAP_PASSWORD = 'qwerty$4'
   base_dn = 'DC=at-consulting.,DC=ru'
   ldap_filter = 'userPrincipalName=vmtest@at-consulting.ru' % username
   attrs = ['memberOf']
   try:
       # build a client
       ldap_client = ldap.initialize(LDAP_SERVER)
       # perform a synchronous bind
       ldap_client.set_option(ldap.OPT_REFERRALS,0)
       ldap_client.simple_bind_s(LDAP_USERNAME, LDAP_PASSWORD)
   except ldap.INVALID_CREDENTIALS:
       ldap_client.unbind()
       return 'Wrong username ili password'
   except ldap.SERVER_DOWN:
       return 'AD server not awailable'
   # all is well
   # get all user groups and store it in cerrypy session for future use
   cherrypy.session[username] = str(ldap_client.search_s(base_dn,
                   ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1]['memberOf'])
   ldap_client.unbind()
   return None

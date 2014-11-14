import ldap
# -*- coding: utf-8 -*- 

# http://torofimofu.blogspot.ru/2013/11/ldap-python.html
ad = ldap.initialize("ldap://192.168.10.2")
ad.protocol_version = ldap.VERSION3
ad.set_option(ldap.OPT_REFERRALS, 0)
ad.simple_bind_s('vmtest', 'qwerty$4')

basedn = 'DC=at-consulting,DC=ru'
scope = ldap.SCOPE_SUBTREE
#attrlist = ["sAMAccountName", "mail"]
attrlist = ["cn", "mail", "sAMAccountName", "title", "telephoneNumber"]
filterexp = "(&(objectCategory=Person)(sAMAccountName=*)(cn=*))"
#results = ad.search_s(basedn, scope, filterexp, attrlist)
users=[]

'''
for result in results:
    try:
        result[1]["mail"][0]
	print result[1]
        #users.append(dict(login=result[1]["sAMAccountName"][0], email=result[1]["mail"][0], fio=result[1]["cn"][0], job=))
        #print unicode(result, errors='ignore')
    except: #If No MAIL...
        pass
'''


#dn = "sAMAccountName=akrushelnitskiy"
dn = "OU=DIT,DC=at-consulting,DC=ru"
results = ad.search_s(dn, ldap.SCOPE_SUBTREE)
for result in results:
	print result[1]
	print '\n'


print results

#modlist = [(ldap.MOD_REPLACE, telephoneNumber='1111')]
#ad.modify_s(dn, modlist)

ad.unbind_s()

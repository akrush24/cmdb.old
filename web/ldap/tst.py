import ldap

ad = ldap.initialize("ldap://192.168.10.2")
ad.protocol_version = ldap.VERSION3
ad.set_option(ldap.OPT_REFERRALS, 0)
ad.simple_bind_s('vmtest', 'qwerty$4')

basedn = 'DC=at-consulting,DC=ru'
scope = ldap.SCOPE_SUBTREE
#attrlist = ["sAMAccountName", "mail"]
attrlist = ["cn", "mail", "sAMAccountName"]
filterexp = "(&(objectCategory=Person)(sAMAccountName=*)(cn=Кри*))"
results = ad.search_s(basedn, scope, filterexp, attrlist)
users=[]
for result in results:
    try:
        result[1]["mail"][0]
        users.append(dict(login=result[1]["sAMAccountName"][0], email=result[1]["mail"][0], fio=result[1]["cn"][0]))
        print result[0]
    except: #If No MAIL...
        pass
    

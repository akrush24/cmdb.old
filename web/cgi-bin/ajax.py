from requests import Request, Session

#turn post string into dict: 
def parsePOSTstring(POSTstr):
    paramList = POSTstr.split('&')
    paramDict = dict([param.split('=') for param in paramList])
    return paramDict

headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',
     'Referer' : 'http://sportsbeta.ladbrokes.com/football'
    }

#prep the data (POSTstr copied from Firebug raw source)
POSTstr = "moreId=156%23327&facetCount_156%23327=12&event=&N=4294966750&pageType=EventClass&
          pageId=p_football_home_page&type=ajaxrequest&eventIDNav=&removedSelectionNav=&
          currentSelectedId=&form-trigger=moreId"
payload = parsePOSTstring(POSTstr)

#end url
url='http://sportsbeta.ladbrokes.com/view/EventDetailPageComponentController'

#start a session to manage cookies, and visit football page first so referer agrees
s = Session()
s.get('http://sportsbeta.ladbrokes.com/football')
#now visit disired url with headers/data
r = s.post(url, data=payload, headers=headers)

#print output
print r.text #this is empty

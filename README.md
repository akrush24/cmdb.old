# CMDB
* http://cmdb.at-consulting.ru/

## HOST
* hostname: `cmdb.at-consulting.ru (192.168.15.183)`
* user: `cmdb`
* password: `cmdb$4`
* samba: `\\cmdb.at-consulting.ru\cmdb\`

## DB
* name: `cmdb`
* user: `cmdb`
* password: `unix11`
* phpmyadmin: http://cmdb.at-consulting.ru/phpmyadmin

## GIT
### First Setup

```bash
git config --global user.name "ФИО"
git config --global user.email "login@mail.ru"
git remote add origin git@gitlab.at-consulting.ru:it/cmdb.git
```

### Working

```bash
git add -A
git commit -am "comment"
git push -u origin master
```

## Python preinstall
```bash
# apt-get install python-pip
# sudo pip install --allow-external mysql-connector-python mysql-connector-python
```

## Parse Json
http://hayageek.com/jquery-ajax-json-parsejson-post-getjson/

## API
### Types
* /new_type/
* /del_type/<int:id>
* /clear_type/<int:id>
* /get_list_type/

### Options
* /new_option/
* /del_option/<int:id>
* /clear_option/<int:id>
* /get_list_option/

### Dictionaries
* /new_dict/
* /del_dict/<int:id>
* /get_list_dict/

### Resources
* /newres
* /del/<typename>/<hash>, POST: type_id

### Users
* /new_user/
* /del_user/<int:id>
* /get_list_user/
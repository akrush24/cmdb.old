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
apt-get install python-pip
pip install --allow-external mysql-connector-python mysql-connector-python
sudo pip install --allow-external mysql-connector-python   mysql-connector-python
```

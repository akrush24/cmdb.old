<<<<<<< HEAD
# CMDB

## host
* name: cmdb.at-consulting.ru (192.168.15.183)
* user: root
* password: cmdb$4

## DB
* name: cmdb
* user: cmdb
* password: unix11
* phpmyadmin: http://cmdb.at-consulting.ru/phpmyadmin

## GIT
* First Setup

```
git config --global user.name "Крушельницкий Андрей Вячеславович"
git config --global user.email "akrushelnitskiy@at-consulting.ru"
git remote add origin git@gitlab.at-consulting.ru:r/test01.git
```
* Working

```
$ git add -A
$ git commit -am "Add DB folder" 
$ git push -u origin master
```

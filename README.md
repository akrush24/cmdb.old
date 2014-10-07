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
```bash
git config --global user.name "Крушельницкий Андрей Вячеславович"
git config --global user.email "akrushelnitskiy@at-consulting.ru"
git remote add origin git@gitlab.at-consulting.ru:r/test01.git
```
* Working
```bash
$ git add -A
$ git commit -am "Add DB folder" 
$ git push -u origin master
```

```javascript
var s = "JavaScript syntax highlighting";
alert(s);
```

```python
def function():
    #indenting works just fine in the fenced code block
    s = "Python syntax highlighting"
    print s
```

```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
```

```
No language indicated, so no syntax highlighting.
s = "There is no highlighting for this."
But let's throw in a <b>tag</b>.
```

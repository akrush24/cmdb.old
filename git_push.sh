#!/bin/bash
comment=$1
git add -A;
git commit -am "${comment}";
git push -u origin master

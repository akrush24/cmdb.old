#!/bin/bash
comment=$1
if [ ! $comment ];then comment=$(date);fi
git add -A;
git commit -am "${comment}";
git push -u origin master

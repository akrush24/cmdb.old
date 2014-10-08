#!/bin/bash
mysqldump -u cmdb -punix11 cmdb > cmdb.$(date +%Y%M%d%H%M).dump

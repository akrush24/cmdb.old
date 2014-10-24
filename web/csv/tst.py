#!/usr/bin/env python
# -*- coding: UTF-8 -*-# enable debugging
import cgitb
import csv

opt_id={2, 3, 4}
with open('csv', 'r') as f:
    reader = csv.reader(f, delimiter=',', )
    for row in reader:
	for col in row:
		print 'insert into value (option_id, value, res_id) values (%s, %s, %s)' % (opt_id, col, res_id	)

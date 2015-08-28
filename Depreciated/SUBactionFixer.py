#####################
# SUB Action Repair/Fixer
# ###################

# Fixing the sequencing of subbills



import sys
import os
import json
import re
import pprint
import csv
import MySQLdb
import re
import pickle
from operator import itemgetter
import datetime

path1 = "/home/stramp/congress/"
os.chdir(path1)
db = MySQLdb.connect(read_default_file="/etc/mysql/my.cnf",db="cbp_main")

badUPD = "UPDATE actions SET subbill = %(subbill)s WHERE actionID = %(actionID)s"

congs = range(93,114)

for congno in congs:
	print congno
	# Pull All Actions with unknown committee
	cursor0 = db.cursor(MySQLdb.cursors.DictCursor)
	z = cursor0.execute("SELECT * FROM `actions` WHERE `status` LIKE 'COMM' and `cong` = %s",congno)
	badA = cursor0.fetchall()
	cursor0.close()
	badA2 = sorted(badA, key=itemgetter('actionID')) 
	a = badA2[0]
	bid = 0
	date = datetime.date(1973, 1, 1)
	for a in badA2:
		if a['billID'] == bid and a['acted_at']==date:
			inc += 1
			a['subbill'] = inc
			print 'MATCH'
		else:
			inc = 0
			a['subbill'] = inc
			bid = a['billID']
			date = a['acted_at']
			print "NOPE"
	for a in badA2:
		if a['subbill'] != 0:
			cursor1 = db.cursor()
			z = cursor1.execute(badUPD,a)
			cursor1.close()
		else:
			pass
	db.commit()





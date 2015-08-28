#####################
# Action Repair/Fixer
# ###################

# This script is set up to retrieve the text attached
# to an action and then prep for manual updates,
# currently to correct missing committee info.



import sys
import os
import json
import re
import pprint
import csv
import logging
import math
import itertools
import MySQLdb
import re
import pickle
from collections import OrderedDict

path1 = "/home/stramp/data/congress/"
os.chdir(path1)
db = MySQLdb.connect(read_default_file="/etc/mysql/my.cnf",db="legex")


# Pull All Actions with unknown committee
cursor0 = db.cursor(MySQLdb.cursors.DictCursor)
z = cursor0.execute("SELECT * FROM `actions` WHERE `loc` LIKE 'UNKN'")
badA = cursor0.fetchall()
cursor0.close()

badUPD = "UPDATE actions SET phrase = %(line)s WHERE actionID = %(actionID)s"

for r in badA:
	try:
		print r['actionID']
		f = path1+"data/"+str(r['cong'])+"/bills/"+r['billtype']+"/"+r['billtype']+str(r['bill'])+"/data.json"
		file = open(f)
		d = json.load(file)
		r['line']= d['actions'][r['actno']]['text']
		cursor1 = db.cursor()
		z = cursor1.execute(badUPD,r)
		cursor1.close()
	except:
		pass

db.commit()


###################


path1 = "/home/stramp/congress/"
os.chdir(path1)
db = MySQLdb.connect(read_default_file="/etc/mysql/my.cnf",db="legex")



cursor2 = db.cursor(MySQLdb.cursors.DictCursor)
z = cursor2.execute("SELECT * FROM `congress_sessions`")
congs = cursor2.fetchall()
cursor2.close()


datUPD = "UPDATE actions SET goodDate = %(goodDate)s WHERE actionID = %(actionID)s"


for C in congs:
	print C['id']
	cursor0 = db.cursor(MySQLdb.cursors.DictCursor)
	z = cursor0.execute("SELECT * FROM `actions` WHERE cong = %s",C['id'])
	badA = cursor0.fetchall()
	cursor0.close()
	for r in badA:
		#print r['actionID']
		if r['acted_at'] >= C['startDate'] and r['acted_at'] <= C['endDate']:
			r['goodDate'] = 1
		else:
			r['goodDate'] = 0
		cursor3 = db.cursor()
		z = cursor3.execute(datUPD,r)
		cursor3.close()


db.commit()

###################
# Committee Membership
# 113th
###################

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
import yaml
from datetime import datetime
from unidecode import unidecode
import io
import pickle
import urllib
import xmltodict

path1 = "/home/stramp/congress/"
os.chdir(path1)
db = MySQLdb.connect(read_default_file="/etc/mysql/my.cnf",db="cbp_main")

mc = open('committee-membership-current.yaml')
m = yaml.load(mc)

current_cong = 113

CCM = []

for C in m:
	print C
	for row in m[C]:
		r = {}
		r['comm'] = C
		r['thomas'] = row['thomas']
		r['name'] = row['name']
		r['party'] = row['party']
		r['rank'] = row['rank']
		r['cong'] = current_cong
		if 'title' in row:
			r['title'] = row['title']
		else:
			r['title'] = ''
		if len(C) == 6:
			r['subC'] = 1
		else:
			r['subC'] = 0
		CCM.append(r)

commINS = "INSERT INTO auto_committee_assign_new (comm,thomas,name,party,rank,cong,subC,title) VALUES (%(comm)s,%(thomas)s,%(name)s,%(party)s,%(rank)s,%(cong)s,%(subC)s,%(title)s);"

for r in CCM:
		cursor2 = db.cursor() #get DW1 score
		x = cursor2.execute(commINS, r)
		cursor2.close()
		db.commit()



# GovTrack SubC Info

mc2 = open('110committees.xml')

doc = xmltodict.parse(mc2)

# add later for 109H and 110-112 H & S


# create dict
commFetch = "SELECT comm, thomas, title, rank FROM auto_committee_assign_new WHERE subC= 0 AND cong = 113 and thomas = %(thomas)s"


cursor1 = db.cursor(MySQLdb.cursors.DictCursor)
cursor1.execute("SELECT * FROM members WHERE cong=113")
members = cursor1.fetchall()

allM = []
errors = []

for M in members:
	#print M['last'], M['cong']
	M['cChair'] = []
	M['cRank'] = []
	M['cMem'] = []
	M['cSen'] = []
	cursor2 = db.cursor(MySQLdb.cursors.DictCursor)
	g = cursor2.execute(commFetch, M)
	comms = cursor2.fetchall()
	for C in comms:
		try:
			M['cMem'].append(C['comm']) # adds committee code to list of committee memberships
			M['cSen'].append(C['rank'])
			if 'title' in C:
				if C['title'] == 'Chair' or C['title'] == 'Chairman':
					M['ComC'] = 1
					M['cChair'].append(C['comm'])
				elif C['title'] == 'Ranking Member':
					M['ComR'] = 1
					M['cRank'].append(C['comm'])
		except Exception as e:
			#errors.append(e[0:3])
			print e
	allM.append(M)

memDex = [r['ICPSR'] for r in allM]
congDex = [r['cong'] for r in allM]




pickle.dump(allM, open( "113M.p", "wb" ) )


import datetime
from json import JSONEncoder

class DateEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)


with open('commM.txt','w') as outfile:
	json.dump(allM,outfile,cls =DateEncoder)

#filename = path1+'allMembers.csv' # writing each member record to csv
#outputFile = io.open(filename,'wb')
#outputFile.write(u'\ufeff'.encode('utf8')) #supposedly helps with opening in Excel
#writer = csv.DictWriter(outputFile, all[0].keys())
#writer.writeheader()
#for di in all:
#	writer.writerow({k:v for k,v in di.items()})
#
#outputFile.close()

#




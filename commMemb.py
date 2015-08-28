###################
# Committee Membership
###################

# creates a pickle file containing a list of dictionaries
# one for each member in each Congress (think of it like a 
# python native-json). This includes all committee membership known
# across all congresses, 93-113


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

path1 = "/data/congress/data/"
os.chdir(path1)
db = MySQLdb.connect(read_default_file="/etc/mysql/my.cnf",db="legex")


cursor0 = db.cursor(MySQLdb.cursors.DictCursor)
cursor0.execute("SELECT * FROM auto_crosswalk_committees")
CW = cursor0.fetchall()

sc = [r['stewartCode'] for r in CW]
thc = [r['govtrackCode'] for r in CW]



commFetch = "SELECT committee_code, senior_party_member, committee_seniority FROM auto_stewart_assigns WHERE icpsr = %(ICPSR)s AND cong = %(cong)s"
commFetchNEW = "SELECT * FROM auto_committee_assign_new WHERE  cong = %(cong)s AND thomas = %(thomas)s"

cursor1 = db.cursor(MySQLdb.cursors.DictCursor)
cursor1.execute("SELECT * FROM members")
members = cursor1.fetchall()

allM = []
errors = []

for M in members:
	if 'ICPSR' in M:
		print M['last'], M['cong']
		M['ComC'] = 0
		M['ComR'] = 0
		M['sComC'] = 0
		M['sComR'] = 0
		M['cChair'] = []
		M['cRank'] = []
		M['sChair'] = []
		M['sRank'] = []
		M['cMem'] = []
		M['cSen'] = []
		cursor2 = db.cursor(MySQLdb.cursors.DictCursor)
		g = cursor2.execute(commFetch, M)
		comms = cursor2.fetchall()
		cursor3 = db.cursor(MySQLdb.cursors.DictCursor)
		h = cursor3.execute(commFetchNEW, M)
		comms2 = cursor3.fetchall()
		for C in comms:
			if M['cong'] < 113:
				try:
					M['cMem'].append(thc[sc.index(C['committee_code'])]) # adds committee code to list of committee memberships
					M['cSen'].append(C['committee_seniority'])
					if C['senior_party_member'] in range(11,19):
						M['ComC'] = 1
						M['cChair'].append(thc[sc.index(C['committee_code'])])
					
					if C['senior_party_member'] in range(21,25):
						M['ComR'] = 1
						M['cRank'].append(thc[sc.index(C['committee_code'])])
					
					if C['senior_party_member'] in range(31,33):
						M['LeadCham'] = 1
					
					if C['senior_party_member'] in range(41,43):
						M['LeadCham'] = 1
				except Exception as e:
					errors.append(e[0:3])
		for C in comms2:
			if M['cong'] >= 113:
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
					errors.append(e[0:3])
			if C['subC'] == 1:
				if 'title' in C:
						if C['title'] == 'Chair' or C['title'] == 'Chairman':
							M['sComC'] = 1
							M['sChair'].append(C['comm'])
						elif C['title'] == 'Ranking Member':
							M['sComR'] = 1
							M['sRank'].append(C['comm'])
	allM.append(M)


allM = pickle.dump(allM, open( "/data/congress/allM.p", "wb" ) )
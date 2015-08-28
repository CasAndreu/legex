
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

path1 = "/home/stramp/congress/"
os.chdir(path1)
db = MySQLdb.connect(read_default_file="/etc/mysql/my.cnf",db="cbp_main")

allM = pickle.load( open( "allM.p", "rb" ) )
bigDex = ['-'.join((str(r['thomas']),str(r['cong']))) for r in allM]


# Pull All Bills
cursor0 = db.cursor(MySQLdb.cursors.DictCursor)
z = cursor0.execute("SELECT * FROM `billsNEW` WHERE cong >= 106")
badA = cursor0.fetchall()
cursor0.close()

badUPD = "UPDATE billsNEW SET SubChRef = %(SubChRef)s, SubRankRef = %(SubRankRef)s, commRefs = %(commsPretty)s WHERE idNEW = %(idNEW)s"

for r in badA:
	print r['idNEW']
	f = path1+"data/"+str(r['Cong'])+"/bills/"+r['BillType']+"/"+r['BillType']+str(r['BillNum'])+"/data.json"
	file = open(f)
	d = json.load(file)
	if 'committees' in d and d['committees'] is not None and r['SpThomasID']:
		try:
			indX = bigDex.index('-'.join((r['SpThomasID'],str(r['Cong']))))
			spC = allM[indX]
			comms = [t['committee_id'] for t in d['committees']]
			comms2 = list(OrderedDict.fromkeys(comms))
			r['commsPretty'] = ', '.join(comms2)
			sC = [w[0:4] for w in spC['sChair']] # stripping subC IDs to parent id
			sR = [w[0:4] for w in spC['sRank']] # stripping subC IDs to parent id
			for c in comms2:
				if c in sC:
					r['SubChRef'] = 1
				if c in sR:
					r['SubRankRef'] = 1
			cursor1 = db.cursor()
			z = cursor1.execute(badUPD,r)
			cursor1.close()
		except Exception as e:
			print e


db.commit()


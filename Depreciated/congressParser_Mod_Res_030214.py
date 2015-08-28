#################
# Congress Parser
#################

# Given only a congress number, runs all the bills and actions
# for that congress and uploads to MySQL

#######
####### do not run an entire congress without purging the DB of that Congress first!
####### 

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
execfile("actionParser.py")
execfile("binfoParser.py")

## un comment one of these lines to run. First line will allow it to be run from command line.
#cong = sys.argv[1]
congs = range(93,113)

for cong in congs:
	congress= cong
	congt = str(cong)
	print "starting "+ congt

	# create list of all bills/res for a given congress by type
	hconres = [filename for filename in os.listdir(path1+"data/"+str(congress)+"/bills/hconres/") if re.search(r'hconres\d{1,4}', filename) != None]
	hres = [filename for filename in os.listdir(path1+"data/"+str(congress)+"/bills/hres/") if re.search(r'hres\d{1,4}', filename) != None]

	sconres = [filename for filename in os.listdir(path1+"data/"+str(congress)+"/bills/sconres/") if re.search(r'sconres\d{1,4}', filename) != None]
	sres = [filename for filename in os.listdir(path1+"data/"+str(congress)+"/bills/sres/") if re.search(r'sres\d{1,4}', filename) != None]

	#switching to ACTIONS
	print "Now time for actions."
	db = MySQLdb.connect(read_default_file="/etc/mysql/my.cnf",db="cbp_main")
	bigMoves = []

	# Look up CBP ID
	cursor1 = db.cursor(MySQLdb.cursors.DictCursor)
	z = cursor1.execute('SELECT idNEW,BillNum,BillType FROM billsNEW WHERE Cong=%s', (cong))
	#cursor1 = db.cursor() #looks up the bill number from CBP bills table.
	#cursor1.execute('SELECT idNEW FROM billsNEW WHERE BillNum=%s AND Cong=%s AND BillType=%s', (bill, cong, billtype.upper()))
	bIDs = cursor1.fetchall()
	cursor1.close()
	bIDsL = [r['idNEW'] for r in bIDs]
	billDex = [''.join((str(r['BillType']),str(r['BillNum']))) for r in bIDs]
	#billID = bIDsL[billDex.index(''.join((billtype,str(bill))))]


	print "parsing hconres actions"
	for b in hconres:
		 #print b
		 bid = bIDsL[billDex.index(''.join(('hconres',re.sub("[^0-9]", "",b))))]
		 moves = actionParser(re.sub("[^0-9]", "",b),congt,'hconres',bid, path1)
		 bigMoves.append(moves)

	print "parsing hres actions"
	for b in hres:
		 #print b
		 bid = bIDsL[billDex.index(''.join(('hres',re.sub("[^0-9]", "",b))))]
		 moves = actionParser(re.sub("[^0-9]", "",b),congt,'hres',bid, path1)
		 bigMoves.append(moves)

	print "parsing sconres actions"
	for b in sconres:
		 #print b
		 bid = bIDsL[billDex.index(''.join(('sconres',re.sub("[^0-9]", "",b))))]
		 moves = actionParser(re.sub("[^0-9]", "",b),congt,'sconres',bid, path1)
		 bigMoves.append(moves)

	print "parsing sres actions"
	for b in sres:
		 #print b
		 bid = bIDsL[billDex.index(''.join(('sres',re.sub("[^0-9]", "",b))))]
		 moves = actionParser(re.sub("[^0-9]", "",b),congt,'sres',bid, path1)
		 bigMoves.append(moves)

	print "make actions dict flat"
	bigflat = [j for i in bigMoves for j in i]

	actINS = "INSERT INTO actions (billID,bill,cong,billtype,acted_at,loc,status,actno,subbill) VALUES (%(billID)s,%(bill)s,%(cong)s,%(billtype)s,%(acted_at)s,%(loc)s,%(status)s,%(actno)s,%(subbill)s);"

	print "uploading actions to MySQL"
	for k in bigflat:
		cursor2 = db.cursor()
		g = cursor2.execute(actINS, k) # write section characteristics to db
		cursor2.close()

	db.commit()
	db.close()

	print "Done with " + str(cong)



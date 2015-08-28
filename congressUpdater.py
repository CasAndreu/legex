#!/usr/bin/env

#################
# Congress Updater
# Set-up for 114th
#################

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
from operator import itemgetter
import datetime

path1 = "/data/congress/"
os.chdir(path1)
db = MySQLdb.connect(read_default_file="/etc/mysql/my.cnf",db="legex")
execfile("/data/congress/LegExCode/legex-data/actionParser.py")
#execfile("/data/congress/LegExCode/legex-data/binfoParser.py")
execfile("/home/jwilker/andreu/binfoParser.py")

print "loading member info"
allM = pickle.load( open("/home/jwilker/andreu/allM.p", "rb" ) )
bigDex = ['-'.join((str(r['thomas']),str(r['cong']))) for r in allM]

print "loading labeled bills 93-114 congress"
labBills = pickle.load(open('/data/congress/data/labeledBills93-114.p', "rb")) 

## un comment one of these lines to run. First line will allow it to be run from command line.
#cong = sys.argv[1]
cong = 114
congBills = [r for r in labBills if r['Cong']==str(cong)]
congHrBills = [r for r in congBills if r['BillType']=='HR']
congSBills = [r for r in congBills if r['BillType']=='S']
congHrBNumber = [r['BillNum'] for r in congHrBills]
congSBNumber = [r['BillNum'] for r in congSBills]

congress= cong
congt = str(cong)
print "starting "+ congt

# create list of all bills/res for a given congress by type
hr = [filename for filename in os.listdir(path1+"data/"+str(congress)+"/bills/hr/") if re.search(r'hr\d{1,4}', filename) != None]
hconres = [filename for filename in os.listdir(path1+"data/"+str(congress)+"/bills/hconres/") if re.search(r'hconres\d{1,4}', filename) != None]
hjres = [filename for filename in os.listdir(path1+"data/"+str(congress)+"/bills/hjres/") if re.search(r'hjres\d{1,4}', filename) != None]
hres = [filename for filename in os.listdir(path1+"data/"+str(congress)+"/bills/hres/") if re.search(r'hres\d{1,4}', filename) != None]

s = [filename for filename in os.listdir(path1+"data/"+str(congress)+"/bills/s/") if re.search(r's\d{1,4}', filename) != None]
sconres = [filename for filename in os.listdir(path1+"data/"+str(congress)+"/bills/sconres/") if re.search(r'sconres\d{1,4}', filename) != None]
sjres = [filename for filename in os.listdir(path1+"data/"+str(congress)+"/bills/sjres/") if re.search(r'sjres\d{1,4}', filename) != None]
sres = [filename for filename in os.listdir(path1+"data/"+str(congress)+"/bills/sres/") if re.search(r'sres\d{1,4}', filename) != None]



# Look up idOLD
cursor0 = db.cursor(MySQLdb.cursors.DictCursor)
cursor0.execute('SELECT id,BillNum,BillType FROM cbp_main.bills WHERE Cong=%s', (cong))
bIDs = cursor0.fetchall()
cursor0.close()
bIDsOLD = [r['id'] for r in bIDs]
billDex0 = [''.join((str(r['BillType']),str(r['BillNum']))) for r in bIDs]
#bid = bIDsOLD[billDex0.index(''.join((billtype.upper(),str(bill))))]


# Look up idNEW
cursor1 = db.cursor(MySQLdb.cursors.DictCursor)
x = cursor1.execute('SELECT idNEW,BillNum,BillType FROM billsNEW WHERE Cong=%s', (cong))
bIDs2 = cursor1.fetchall()
cursor1.close()
bIDsNEW = [r['idNEW'] for r in bIDs2]
billDex1 = [''.join((str(r['BillType']),str(r['BillNum']))) for r in bIDs2]
#bid = bIDsOLD[billDex0.index(''.join((billtype.upper(),str(bill))))]

newBills = []
updBills = []

print "parsing hr"
for b in hr:
	try:
		bidNEW = bIDsNEW[billDex1.index(b)]
		NEW = 0
	except ValueError:
		NEW = 1
	if NEW == 1:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'hr',bid,path1)
		print "NEW: " + b
		newBills.append(bill)
	if NEW==0:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'hr',bid,path1)
		bill['idNEW'] = bidNEW
		print "UPDATED: " + b
		updBills.append(bill)


print "parsing hconres"
for b in hconres:
	try:
		bidNEW = bIDsNEW[billDex1.index(b)]
		NEW = 0
	except ValueError:
		NEW = 1
	if NEW == 1:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'hconres',bid,path1)
		print "NEW: " + b
		newBills.append(bill)
	if NEW==0:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'hconres',bid,path1)
		bill['idNEW'] = bidNEW
		print "UPDATED: " + b
		updBills.append(bill)

print "parsing hjres"
for b in hjres:
	try:
		bidNEW = bIDsNEW[billDex1.index(b)]
		NEW = 0
	except ValueError:
		NEW = 1
	if NEW == 1:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'hjres',bid,path1)
		print "NEW: " + b
		newBills.append(bill)
	if NEW==0:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'hjres',bid,path1)
		bill['idNEW'] = bidNEW
		print "UPDATED: " + b
		updBills.append(bill)

print "parsing hres"
for b in hres:
	try:
		bidNEW = bIDsNEW[billDex1.index(b)]
		NEW = 0
	except ValueError:
		NEW = 1
	if NEW == 1:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'hres',bid,path1)
		print "NEW: " + b
		newBills.append(bill)
	if NEW==0:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'hres',bid,path1)
		bill['idNEW'] = bidNEW
		print "UPDATED: " + b
		updBills.append(bill)

print "parsing s"
for b in s:
	try:
		bidNEW = bIDsNEW[billDex1.index(b)]
		NEW = 0
	except ValueError:
		NEW = 1
	if NEW == 1:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'s',bid,path1)
		print "NEW: " + b
		newBills.append(bill)
	if NEW==0:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'s',bid,path1)
		bill['idNEW'] = bidNEW
		print "UPDATED: " + b
		updBills.append(bill)

print "parsing sconres"
for b in sconres:
	try:
		bidNEW = bIDsNEW[billDex1.index(b)]
		NEW = 0
	except ValueError:
		NEW = 1
	if NEW == 1:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'sconres',bid,path1)
		print "NEW: " + b
		newBills.append(bill)
	if NEW==0:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'sconres',bid,path1)
		bill['idNEW'] = bidNEW
		print "UPDATED: " + b
		updBills.append(bill)

print "parsing sjres"
for b in sjres:
	try:
		bidNEW = bIDsNEW[billDex1.index(b)]
		NEW = 0
	except ValueError:
		NEW = 1
	if NEW == 1:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'sjres',bid,path1)
		print "NEW: " + b
		newBills.append(bill)
	if NEW==0:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'sjres',bid,path1)
		bill['idNEW'] = bidNEW
		print "UPDATED: " + b
		updBills.append(bill)

print "parsing sres"
for b in sres:
	try:
		bidNEW = bIDsNEW[billDex1.index(b)]
		NEW = 0
	except ValueError:
		NEW = 1
	if NEW == 1:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'sres',bid,path1)
		print "NEW: " + b
		newBills.append(bill)
	if NEW==0:
		try:
			bid = bIDsOLD[billDex0.index(b.upper())]
		except ValueError:
			bid = 0
		bill = binfoParser(re.sub("[^0-9]", "",b),congt,'sres',bid,path1)
		bill['idNEW'] = bidNEW
		print "UPDATED: " + b
		updBills.append(bill)
  
print 'Length newBills: ' + str(len(newBills))
print 'Length updBills: ' + str(len(updBills))

memref= 0
rankref= 0
subrankref =0
chref = 0
subchref = 0 
for p in updBills:
    if p['MemRef']==1:
        memref += 1
    if p['RankRef']==1:
        rankref += 1
    if p['SubRankRef']==1:
        subrankref += 1
    if p['ChRef']==1:
        chref += 1
    if p['SubChRef']==1:
        subchref += 1

print 'MemRef = ' + str(memref)
print 'ChRef = ' + str(chref)
print 'RankRef = ' + str(rankref)
print 'SubChRef = ' + str(subchref)
print 'SubRankRef = ' + str(subrankref)

billINS = "INSERT INTO billsNEW (BillNum,BillType,Cong,IntrDate,ShortTitle,OfficialTitle,PopTitle,SpThomasID,SpName,SpState,SpDist,UpdatedAt,CoSpThID,PLawNo,idOLD,ChRef,RankRef,MemRef) VALUES (%(BNum)s,%(BillType)s,%(Cong)s,%(Intro)s,%(ShortTitle)s,%(OfficialTitle)s,%(PopTitle)s,%(SpThomasID)s,%(SpName)s,%(SpState)s,%(SpDist)s,%(UpdatedAt)s,%(CoSpThID)s,%(PLawNo)s,%(billID)s,%(ChRef)s,%(RankRef)s,%(MemRef)s,%(SubChRef)s,%(SubRankRef)s;"
billUPD = "UPDATE billsNEW SET ShortTitle = %s, OfficialTitle = %s,PopTitle = %s,CoSpThID = %s,PLawNo = %s, ChRef=%s, RankRef=%s, MemRef=%s, SubChRef=%s, SubRankRef=%s WHERE  idNew = %s;"


print "uploading NEW bills to MySQL"
a = 0
for k in newBills:
	#print a
	a +=1
	if 'CoSpThID' in k:
		k['CoSpThID'] = ','.join(k['CoSpThID'])
	else:
		k['CoSpThID'] = ''
	if 'PLawNo' not in k:
		k['PLawNo'] = ''
	cursor2 = db.cursor()
	k = cursor2.execute(billINS, k) # write bill characteristics to db
	cursor2.close()

db.commit()

print "UPDATING bills"
a = 0
for k in updBills:
	#print a
	a +=1
	if 'CoSpThID' in k:
		k['CoSpThID'] = ','.join(k['CoSpThID'])
	else:
		k['CoSpThID'] = ''
	if 'PLawNo' not in k:
		k['PLawNo'] = ''
	data = (k['ShortTitle'],k['OfficialTitle'],k['PopTitle'],k['CoSpThID'],k['PLawNo'],k['ChRef'],k['RankRef'],k['MemRef'],k['SubChRef'],k['SubRankRef'],k['idNEW'])
	cursor2 = db.cursor()
	output = cursor2.execute(billUPD, data) # write bill characteristics to db
	cursor2.close()

db.commit()

print("Updating -Major- and -Minor- variables")

# Codes the PAP Major and Minor variables for each bill. It takes the 
#		info from a pickle file ('/data/congress/data/labeledBills93-114.p').
#		In the file there is only PAP codes for some HR ans S bills of the
#		114th Congress. The most recent bills still have to be coded. Once
#		they are coded, the pickled file should be updated. 

for bill in congBills:
    major = bill['Major']
    minor = bill['Minor']
    billNum = bill['BillNum']
    billType = bill['BillType'].lower()
    cong = bill['Cong']
    cursor = db.cursor()
    output = cursor.execute("UPDATE billsNEW SET Major=%s, Minor=%s WHERE Cong=%s AND BillType=%s AND BillNum=%s",(major,minor,cong,billType,billNum))
    cursor.close()

db.commit()



print("Updating -MinorBill- and -ImpBill- variables")


# Updated the info about whether a bill is considered as Minor or Important
q1 = "UPDATE billsNEW SET ImpBill= '0'WHERE Cong=%s;"
q2 = "UPDATE billsNEW SET MinorBill= '0' WHERE Cong=%s;"
q3 = "UPDATE billsNEW SET ImpBill=NULL WHERE BillType IN ('hres','sres','hjres','sjres','hconres','sconres') and Cong=%s;"
q4 = "UPDATE billsNEW SET MinorBill=NULL WHERE BillType IN ('hres','sres','hjres','sjres','hconres','sconres') and Cong=%s;"
q5 = "UPDATE billsNEW SET MinorBill='1' WHERE Major='99' AND BillType IN ('hr','s') AND Cong=%s;"
q6 = "UPDATE billsNEW SET MinorBill=1 WHERE OfficialTitle LIKE '%medal%' OR OfficialTitle LIKE '%coin%' OR OfficialTitle LIKE '%designate%' OR OfficialTitle LIKE'%name%' OR OfficialTitle LIKE'%techincal correction*%' OR OfficialTitle LIKE'%stamp%' OR OfficialTitle LIKE '%land exchange%'OR OfficialTitle LIKE'%suspend temporarily%' OR OfficialTitle LIKE'%extend the temporary%' OR OfficialTitle LIKE '%boundar*%' OR OfficialTitle LIKE '%exchange of land*%' AND Cong=113;"
q7= "UPDATE billsNEW SET ImpBill='1' WHERE MinorBill='0' AND Cong=%s;"

queries = [q1,q2,q3,q4,q5,q6,q7]

count = 1
for q in queries:
    cursorX = db.cursor()
    if count == 6:
    	output = cursorX.execute(q)
    else:
    	output = cursorX.execute(q,cong)
    cursorX.close()
    count = count + 1

db.commit()


#switching to ACTIONS
print "Now time for actions."
db = MySQLdb.connect(read_default_file="/etc/mysql/my.cnf",db="legex")


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

bigMoves = []
print "parsing hr actions"
for b in hr:
	 #print b
	 bid = bIDsL[billDex.index(''.join(('hr',re.sub("[^0-9]", "",b))))]
	 moves = actionParser(re.sub("[^0-9]", "",b),congt,'hr',bid,path1)
	 bigMoves.append(moves)

print "parsing hconres actions"
for b in hconres:
	 #print b
	 bid = bIDsL[billDex.index(''.join(('hconres',re.sub("[^0-9]", "",b))))]
	 moves = actionParser(re.sub("[^0-9]", "",b),congt,'hconres',bid,path1)
	 bigMoves.append(moves)

print "parsing hrjres actions"
for b in hjres:
	 #print b
	 bid = bIDsL[billDex.index(''.join(('hjres',re.sub("[^0-9]", "",b))))]
	 moves = actionParser(re.sub("[^0-9]", "",b),congt,'hjres',bid,path1)
	 bigMoves.append(moves)

print "parsing hres actions"
for b in hres:
	 #print b
	 bid = bIDsL[billDex.index(''.join(('hres',re.sub("[^0-9]", "",b))))]
	 moves = actionParser(re.sub("[^0-9]", "",b),congt,'hres',bid,path1)
	 bigMoves.append(moves)

print "parsing s actions"
for b in s:
	 #print b
	 bid = bIDsL[billDex.index(''.join(('s',re.sub("[^0-9]", "",b))))]
	 moves = actionParser(re.sub("[^0-9]", "",b),congt,'s',bid,path1)
	 bigMoves.append(moves)

print "parsing sconres actions"
for b in sconres:
	 #print b
	 bid = bIDsL[billDex.index(''.join(('sconres',re.sub("[^0-9]", "",b))))]
	 moves = actionParser(re.sub("[^0-9]", "",b),congt,'sconres',bid,path1)
	 bigMoves.append(moves)

print "parsing sjres actions"
for b in sjres:
	 #print b
	 bid = bIDsL[billDex.index(''.join(('sjres',re.sub("[^0-9]", "",b))))]
	 moves = actionParser(re.sub("[^0-9]", "",b),congt,'sjres',bid,path1)
	 bigMoves.append(moves)

print "parsing sres actions"
for b in sres:
	 #print b
	 bid = bIDsL[billDex.index(''.join(('sres',re.sub("[^0-9]", "",b))))]
	 moves = actionParser(re.sub("[^0-9]", "",b),congt,'sres',bid,path1)
	 bigMoves.append(moves)



# Look up action count per bill
cursor1 = db.cursor(MySQLdb.cursors.DictCursor)
z = cursor1.execute('SELECT COUNT(*) AS `Rows`, `billID` FROM `actions` WHERE cong = %s GROUP BY `billID` ORDER BY `billID`', (cong))
aCounts = cursor1.fetchall()
cursor1.close()
abIDs = [r['billID'] for r in aCounts]

actINS = "INSERT INTO actions (billID,bill,cong,billtype,acted_at,loc,status,actno,subbill) VALUES (%(billID)s,%(bill)s,%(cong)s,%(billtype)s,%(acted_at)s,%(loc)s,%(status)s,%(actno)s,%(subbill)s);"
actINS2 = "INSERT INTO actions (billID,bill,cong,billtype,acted_at,loc,status,actno,subbill,manUpdate) VALUES (%(billID)s,%(bill)s,%(cong)s,%(billtype)s,%(acted_at)s,%(loc)s,%(status)s,%(actno)s,%(subbill)s,%(manUpdate)s);"

for b in bigMoves:
	bIDNEW = b[0]['billID']
	try:
		actionCount = aCounts[abIDs.index(bIDNEW)]['Rows']
	except ValueError:
		actionCount = 0
	if actionCount == 0:
		for k in b:
			cursor2 = db.cursor()
			g = cursor2.execute(actINS, k) # write section characteristics to db
			cursor2.close()
			db.commit()
	if actionCount < len(b): # actionCount is currently in db, b is the count of newly processed actions
		cursor1 = db.cursor(MySQLdb.cursors.DictCursor)
		z = cursor1.execute('SELECT * FROM actions WHERE billid = %s', (bIDNEW))
		actionsCurr = list(cursor1.fetchall())
		cursor1.close()
		completeActions = actionsCurr + b[actionCount:]
		cursor3 = db.cursor()
		z = cursor3.execute('DELETE FROM actions WHERE billid = %s', (bIDNEW))
		cursor3.close()
		db.commit()
		for k in b:
			if 'manUpdate' not in k:
				k['manUpdate'] = 0
			cursor4 = db.cursor()
			g = cursor4.execute(actINS2, k) # write section characteristics to db
			cursor4.close()
		db.commit()

# counting sub-actions
print "Organizing Sub-Actions"

cursor0 = db.cursor(MySQLdb.cursors.DictCursor)
z = cursor0.execute("SELECT * FROM `actions` WHERE `status` LIKE 'COMM' and `cong` = %s",congt)
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
		#print 'MATCH'
	else:
		inc = 0
		a['subbill'] = inc
		bid = a['billID']
		date = a['acted_at']
		#print "NOPE"

badUPD = "UPDATE actions SET subbill = %(subbill)s WHERE actionID = %(actionID)s"
for a in badA2:
	if a['subbill'] != 0:
		cursor1 = db.cursor()
		z = cursor1.execute(badUPD,a)
		cursor1.close()
	else:
		pass

db.commit()



db.close()

print "Done with " + str(cong)
###################
# Member Upload
###################

# preps and uploads data from congress-legislators
# github to our mysql server in a format of
# one MoC-term per row.

#### do not re-run without preserving existing manual changes to member info!

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

path1 = "/home/stramp/congress/"
os.chdir(path1)
db = MySQLdb.connect(read_default_file="/etc/mysql/my.cnf",db="legex")



# local testing
path1 = "/Users/nstramp/Documents/UW/Research/BillFlowProject/members/"
os.chdir(path1)


f = open("legislators-current.yaml") # from congress-legislators github
docs = yaml.load(f)

#f2 = open("legislators-historical.yaml") # from congress-legislators github ** use pickl file on server
#docs2 = yaml.load(f2)
docs2 = pickle.load( open( "docs2.p", "rb" ) )

def congPicker(date): # creates best estimate for Congress No from a starting date
	year = int(date[0:4])
	return int(math.ceil(year/2.0)-894)

def congPickerY(year): # creates best estimate of Congress No from a year
	return int(math.ceil(year/2.0)-894)



execfile('memberParser.py')


all = []
for i in docs:
	all = all + memberParser(i)

for j in docs2:
	all = all + memberParser(j)

for d in all:
	d['first'] = unidecode(d['first']) 
	d['last'] = unidecode(d['last']) 

memINS = "INSERT INTO members (ICPSR,thomas,govtrack,cong,first,last,gender,type,state,start,end,district,class,party) VALUES (%(icpsr)s,%(thomas)s,%(govtrack)s,%(cong)s,%(first)s,%(last)s,%(gender)s,%(type)s,%(state)s,%(start)s,%(end)s,%(district)s,%(class)s,%(party)s);"

for r in all:
	if r['cong'] == 113:
		cursor2 = db.cursor() #get DW1 score
		cursor2.execute(memINS, r)
		cursor2.close()
		db.commit()


######## UPDATING COMC and COMR (subs)

allM = pickle.load( open( "allM.p", "rb" ) )

memUPD = "UPDATE members SET sComC = %(ComC)s, sComR = %(ComR)s WHERE thomas = %(thomas)s AND cong = %(cong)s;"

for r in allM:
	if r['sComC'] == 1 or r['sComR'] == 1:
		print r['thomas']
		cursor2 = db.cursor() #get DW1 score
		x = cursor2.execute(memUPD, r)
		cursor2.close()
		db.commit()




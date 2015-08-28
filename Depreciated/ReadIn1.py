###################
# GPO TO BillFlow
# Initial Attempt 
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

# local testing
path1 = "/Users/nstramp/Documents/UW/Research/BillFlowProject/Samples/"
os.chdir(path1)
execfile("/Users/nstramp/Documents/UW/Research/BillFlowProject/Code/binfoParser.py")

#### single bill testing
bill = '65'
cong = 110
billtype = 'hjres'

path1 = "/Users/nstramp/Documents/UW/Research/BillFlowProject/Samples/"
f = path1+str(cong)+billtype+bill+'.json'
file = open(f)
d = json.load(file)
z = 0
actions = []
billID = 000001
execfile('/Users/nstramp/Documents/UW/Research/BillFlowProject/Code/action_parser_basic.py')
pprint.pprint(actions)



# SERVER SIDE

path1 = "/home/stramp/congress/"
os.chdir(path1)
db = MySQLdb.connect(read_default_file="/etc/mysql/my.cnf",db="cbp_main")
execfile("actionParser.py")
execfile("binfoParser.py")



#### single bill testing
bill = '92'
cong = 110
billtype = 'hjres'
test = actionParser(bill,cong,billtype)
test2 = binfoParser('92',110,'hjres')
f = path1+"data/"+str(cong)+"/bills/"+billtype+"/"+billtype+str(bill)+"/data.json"
file = open(f)
d = json.load(file)


#filename = path1+'110SActions121313.csv' # writing each bill to csv
#outputFile = open(filename,'wb')
#outputFile.write(u'\ufeff'.encode('utf8')) #supposedly helps with opening in Excel
#writer = csv.DictWriter(outputFile, bigflat[0].keys())
#writer.writeheader()
#for di in bigflat:
#	writer.writerow({k:v for k,v in di.items()})
#
#outputFile.close()

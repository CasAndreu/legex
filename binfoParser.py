##################
# Bill Info Parser
##################

# Given a bill as well as the path to the .json files and the old billID
# returns the characteristics of the bill
# including all referral chair/mem/rank variables at comm and subcomm


def binfoParser(bill,cong,billtype,idold,path1):
	try:
		f = path1+"data/"+str(cong)+"/bills/"+billtype+"/"+billtype+str(bill)+"/data.json"
		file = open(f)
		d = json.load(file)
		billID = idold
		b = {'billID': billID, 'BNum': int(d['number']),
		'Cong':int(d['congress']),
		'BillType': d['bill_type'],
		'Intro': d['introduced_at'],
		'ShortTitle': d['short_title'],
		'OfficialTitle': d['official_title'],
		'PopTitle': d['popular_title'],
		'UpdatedAt': d['updated_at'],
		'MemRef': 0,'RankRef': 0,'ChRef': 0}
		if 'committees' in d and d['committees'] is not None:
			comms = [r['committee_id'] for r in d['committees']]
			comms2 = list(OrderedDict.fromkeys(comms))
			b['committees'] = ','.join(comms2)
			b['commsPretty'] = ', '.join(comms2)
		if 'sponsor' in d and d['sponsor'] is not None:
			b['SpThomasID'] = d['sponsor']['thomas_id']
			b['SpName'] = d['sponsor']['name']
			b['SpState'] = d['sponsor']['state']
			b['SpDist'] = d['sponsor']['district']
		else:
			b['SpThomasID'] = ''
			b['SpName'] = ''
			b['SpState'] = ''
			b['SpDist'] = ''
		if 'committees' in d and d['committees'] is not None and b['SpThomasID']:
			try:
				indX = bigDex.index('-'.join((b['SpThomasID'],str(b['Cong']))))
				spC = allM[indX]
				sC = [w[0:4] for w in spC['sChair']] # stripping subC IDs to parent id
				sR = [w[0:4] for w in spC['sRank']] # stripping subC IDs to parent id
				for c in comms2:
					if c in spC['cMem']:
						b['MemRef'] = 1
					if c in spC['cRank']:
						b['RankRef'] = 1
					if c in spC['cChair']:
						b['ChRef'] = 1
					if c in sC:
						r['SubChRef'] = 1
					if c in sR:
						r['SubRankRef'] = 1
			except Exception as e:
				print e
		if 'cosponsors' in d and any(d['cosponsors']):
			b['CoSpThID'] =  [e['thomas_id'] for e in d['cosponsors']]
		else:
			b['CoSpThID'] = ''
		if 'enacted_as' in d and d['enacted_as'] is not None:
			b['PLawNo'] = int(d['enacted_as']['number']) 
		else:
			b['PLawNo'] = ''
	except Exception as e:
		print "Whoops! B "+bill+" "+str(e)
	return(b)
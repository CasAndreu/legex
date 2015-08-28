##################
# Action Parser
##################

# Given a bill as well as the path to the .json files, parses 
# all the bills actions, scraping the ones we want and
# returns a dictionary with all the actions


def actionParser(bill,cong,billtype,bid,path1):
	try:
		f = path1+"data/"+str(cong)+"/bills/"+billtype+"/"+billtype+str(bill)+"/data.json"
		file = open(f)
		d = json.load(file)
		z = 0
		billID = bid
		actions = []
		# introduction date
		actions.append({'billID': billID,'bill': bill,'cong': cong,'billtype':billtype,'acted_at': d['actions'][0]['acted_at'],'loc': billtype[0].upper()+'INT','status': 'INT', 'actno': z,'subbill': 0})
		binfo = {'billID': billID,'bill': bill,'cong': cong,'billtype':billtype}
		sbc = 0
		for i in d['actions']: # all actions
			a = {}
			if i['type'] == 'referral' and 'Subcommittee' not in i['text']: # Assigned to committees, excl subs
				#sbc +=1
				if 'committees' in i:
					a = {'acted_at':i['acted_at'][0:10] ,'loc':i['committees'][0],'status':'COMM', 'actno': z,'subbill': 0}
				else:
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'UNKN','status':'COMM', 'actno': z,'subbill': 0}
			elif i['type'] == 'action': 
				if 'Reported' in i['text'] and 'committees' in i: # Reported by committee
#					match = next((l['subbill'] for l in actions if l['loc'] == i['committees'][0]), None) # <- moved sub-bill to external process
					a = {'acted_at':i['acted_at'][0:10] ,'loc':i['committees'][0],'status':'REP', 'actno': z,'subbill': 0}
				elif 'Reported' in i['text'] and 'committees' not in i: # Reported by committee
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'UNKN','status':'REP', 'actno': z,'subbill': 0}
				if 'discharged' in i['text'] and 'committees' in i: # Reported by committee
					match = next((l['subbill'] for l in actions if l['loc'] == i['committees'][0]), None) # finds correct subbill number for comm
					a = {'acted_at':i['acted_at'][0:10] ,'loc':i['committees'][0],'status':'DISC', 'actno': z,'subbill': 0}
				elif 'discharged' in i['text'] and 'committees' not in i: # Reported by committee
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'UNKN','status':'DISC', 'actno': z,'subbill': 0}
				elif 'Considered under suspension of the rules' in i['text'] or 'House suspend the rules' in i['text']: # Consider Under Suspension
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'SUSP','status':'CONS', 'actno': z,'subbill': 0}
				elif 'Rule' in i['text'] and 'passed House' in i['text']: # House Rule passed on floor
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'HFLR', 'status':'RULP', 'actno': z,'subbill': 0}
				elif i['text'] == 'Conference held.': # specific conference language from 110 HR 2419
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'CONF','status':'CONF', 'actno': z,'subbill': 0}
				elif 'Conference report' in i['text'] and 'filed' in i['text']: # specific conference language from 110 HR 2419
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'CONF','status':'CREP', 'actno': z, 'subbill':0}
				elif 'H' in i['text'] and 'references' in i: # House Floor Consideration
					if len(i['references'])>0:
						if i['references'][0]['type'] == 'consideration' and 'H' in i['references'][0]['reference'] and 'instruct conferees' not in i['text']:
							a = {'acted_at':i['acted_at'][0:10] ,'loc':'HFLR','status':'CONS', 'actno': z, 'subbill':0}
				elif 'S' in i['text'] and 'references' in i: # Senate Floor Consideration
					if len(i['references'])>0:
						if i['references'][0]['type'] == 'consideration' and 'S' in i['references'][0]['reference'] and 'instruct conferees' not in i['text']:
							a = {'acted_at':i['acted_at'][0:10] ,'loc':'SFLR','status':'CONS', 'actno': z, 'subbill':0}
			elif i['type'] == 'calendar' and 'calendar' in i: # Placed on calendar
				if i['calendar'] == 'Senate Legislative':
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'SCAL','status':'CAL', 'actno': z, 'subbill':0}
				else:
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'HCAL','status':'CAL', 'actno': z, 'subbill':0}
			elif i['type'] == 'vote' and 'status' in i:
				if i['how'] == 'by Unanimous Consent' and i['vote_type'] == 'vote2' and i['result'] == 'pass':
					if i['status'] == 'PASSED:CONCURRENTRES' or d['status'] == 'PASSED:SIMPLERES':
						a = {'acted_at':i['acted_at'][0:10] ,'loc':'SUNC','status':'RESA', 'actno': z, 'subbill':0}
					else: 
						a = {'acted_at':i['acted_at'][0:10] ,'loc':'SUNC','status':'PASS', 'actno': z, 'subbill':0}
					b = {'acted_at':i['acted_at'][0:10] ,'loc':'SUNC','status':'CONS', 'actno': z, 'subbill':0}
					b.update(binfo)
					actions.append(b.copy())
				elif i['how'] == 'by Unanimous Consent' and i['vote_type'] == 'vote' and i['result'] == 'pass':
					if i['status'] == 'PASSED:CONCURRENTRES' or d['status'] == 'PASSED:SIMPLERES':
						a = {'acted_at':i['acted_at'][0:10] ,'loc':'SUNC','status':'RESA', 'actno': z, 'subbill':0}
					else: 
						a = {'acted_at':i['acted_at'][0:10] ,'loc':'SUNC','status':'PASSO', 'actno': z, 'subbill':0}
					b = {'acted_at':i['acted_at'][0:10] ,'loc':'SUNC','status':'CONS', 'actno': z, 'subbill':0}
					b.update(binfo)
					actions.append(b.copy())
				elif 'suspension' in i and i['suspension'] is not None:
					if i['status'] == 'PASSED:CONCURRENTRES' or d['status'] == 'PASSED:SIMPLERES':
						a = {'acted_at':i['acted_at'][0:10] ,'loc':'HSUS','status':'RESA', 'actno': z, 'subbill':0}
					elif i['vote_type'] == 'vote' and i['status'] == 'PASSED:BILL':
						a = {'acted_at':i['acted_at'][0:10] ,'loc':'HSUS','status':'PASS', 'actno': z, 'subbill':0}
					elif i['vote_type'] == 'vote' and i['result'] == 'pass':
						a = {'acted_at':i['acted_at'][0:10] ,'loc':'HSUS','status':'PASSO', 'actno': z, 'subbill':0}
					elif i['vote_type'] == 'vote2' and i['result'] == 'pass':
						a = {'acted_at':i['acted_at'][0:10] ,'loc':'HSUS','status':'PASS', 'actno': z, 'subbill':0}
				elif i['status'] == 'PASS_OVER:HOUSE': # Floor vote, House, sent to Senate
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'HFLR','status':'PASSO', 'actno': z, 'subbill':0}
				elif i['status'] == 'PASS_BACK:SENATE': # Floor vote, Senate, BACK to House
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'SFLR','status':'PASSB', 'actno': z, 'subbill':0}
				elif i['status'] == 'PASS_OVER:SENATE': # Floor vote, Senate, sent to House
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'SFLR','status':'PASSO', 'actno': z, 'subbill':0}
				elif i['status'] == 'PASS_BACK:HOUSE': # Floor vote, House, BACK to Senate
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'HFLR','status':'PASSB', 'actno': z, 'subbill':0}
				elif i['status'] == 'PASSED:BILL' and i['where'] == 'h': # Passed both chambers 2nd House
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'HFLR','status':'PASS', 'actno': z, 'subbill':0}
				elif i['status'] == 'PASSED:BILL' and i['where'] == 's': # Passed both chambers 2nd Senate
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'SFLR','status':'PASS', 'actno': z, 'subbill':0}
				elif i['status'] == 'PASSED:SIMPLERES' and i['where'] == 'h': # Passed both chambers 2nd House
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'HFLR','status':'RESA', 'actno': z, 'subbill':0}
				elif i['status'] == 'PASSED:CONCURRENTRES' and i['where'] == 'h': # Passed both chambers 2nd Senate
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'HFLR','status':'RESA', 'actno': z, 'subbill':0}
				elif i['status'] == 'PASSED:SIMPLERES' and i['where'] == 's': # Passed both chambers 2nd House
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'SFLR','status':'RESA', 'actno': z, 'subbill':0}
				elif i['status'] == 'PASSED:CONCURRENTRES' and i['where'] == 's': # Passed both chambers 2nd Senate
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'SFLR','status':'RESA', 'actno': z, 'subbill':0}
				elif i['status'] == 'CONFERENCE:PASSED:HOUSE' and i['where'] == 'h': # House passes conf first
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'HFLR','status':'PASSC', 'actno': z, 'subbill':0}
				elif i['status'] == 'CONFERENCE:PASSED:SENATE' and i['where'] == 's': # Senate passed conf first
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'SFLR','status':'PASSC', 'actno': z, 'subbill':0}
				elif i['status'] == 'VETOED:OVERRIDE_PASS_OVER:HOUSE' and i['where'] == 'h': # Senate passed conf first
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'HFLR','status':'PASSV', 'actno': z, 'subbill':0}
			elif i['type'] == 'topresident' and 'President' in i['text']:
				a = {'acted_at':i['acted_at'][0:10] ,'loc':'PDSK','status':'WAIT', 'actno': z, 'subbill':0}
			elif i['type'] == 'signed':
				a = {'acted_at':i['acted_at'][0:10] ,'loc':'PDSK','status':'SIGN', 'actno': z, 'subbill':0}
			elif i['type'] == 'vetoed':
				a = {'acted_at':i['acted_at'][0:10] ,'loc':'PDSK','status':'VETO', 'actno': z, 'subbill':0}
			elif i['type'] == 'enacted':
				a = {'acted_at':i['acted_at'][0:10] ,'loc':'LAW','status':'LAW', 'actno': z, 'subbill':0}
			elif 'vote_type' in i and 'status' not in i:
				if i['vote_type'] == 'override':
					a = {'acted_at':i['acted_at'][0:10] ,'loc':'SFLR','status':'PASSV2', 'actno': z, 'subbill':0}
			if any(a): # if a (dictionary) exists in this loop
				a.update(binfo)
				if not (actions[-1]['status']==a['status'] and actions[-1]['loc']==a['loc']): # if status & loop unique, write
					actions.append(a.copy())
			z +=1
		if d['status'] == 'PASSED:CONCURRENTRES' or d['status'] == 'PASSED:SIMPLERES':
			a = {'acted_at':i['acted_at'][0:10] ,'loc':'RESA','status':'RESA', 'actno': z, 'subbill':0}	
			a.update(binfo)
			actions.append(a.copy())				
	except Exception as e:
		print "Whoops! A "+bill+" "+str(e)
	return(actions)
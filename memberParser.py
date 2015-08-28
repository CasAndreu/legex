##################
# Member Parser
##################

# Takes a .yaml file containing info for a MoC
# converts it into a congress-by-congress record and includes various ids and 
# attributes about the person
# returns a dictionary, ready to be loaded into db


def memberParser(leg):
	memb = []
	if int(leg['terms'][-1]['start'][0:4]) > 1965: # skip all members who finished before 1973
		print leg['name']['last']
		if 'thomas' not in leg['id']:
			leg['id']['thomas'] = 0
		if 'icpsr' in leg['id']: # pull out basic member bio information
			if 'gender' in leg['bio']:
				m = {'icpsr':leg['id']['icpsr'],'thomas':leg['id']['thomas'],'govtrack':leg['id']['govtrack'],'first':leg['name']['first'],
				'last':leg['name']['last'],'gender':leg['bio']['gender'] }
			else: 
				m = {'icpsr':leg['id']['icpsr'],'thomas':leg['id']['thomas'],'govtrack':leg['id']['govtrack'],'first':leg['name']['first'],
				'last':leg['name']['last'],'gender':'M' }
		else:
			if 'gender' in leg['bio']:
				m = {'icpsr':0,'thomas':leg['id']['thomas'],'govtrack':leg['id']['govtrack'],'first':leg['name']['first'],
				'last':leg['name']['last'],'gender':leg['bio']['gender'] }
			else: 
				m = {'icpsr':0,'thomas':leg['id']['thomas'],'govtrack':leg['id']['govtrack'],'first':leg['name']['first'],
				'last':leg['name']['last'],'gender':'M' }
		for term in leg['terms']:
			if term['type'] == 'rep':
				if 'district' in term:
					t = {'type': term['type'],'state':term['state'],'start':term['start'],'end':term['end'],
					'district': term['district'],'class':'NA','party':term['party'],'cong': congPicker(term['start'])}
				else:
					t = {'type': term['type'],'state':term['state'],'start':term['start'],'end':term['end'],
					'district': 0,'class':'NA','party':term['party'],'cong': congPicker(term['start'])}
				if t['cong']>92:
					tt = dict(m.items() + t.items())
					memb.append(tt)
			elif term['type'] == 'sen':
				s = int(term['start'][0:4]) # starting year
				e = int(term['end'][0:4]) # ending year
				c = list(set([congPickerY(year) for year in range(s,e)]))
				for no in c:
					t = {'type': term['type'],'state':term['state'],'start':term['start'],'end':term['end'],
					'district': 0,'class':term['class'],'party':term['party'],'cong':no}
					if t['cong']>92:
						tt = dict(m.items() + t.items())
						memb.append(tt)
	return(memb)


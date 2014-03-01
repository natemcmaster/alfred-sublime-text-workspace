import os, alfred, codecs, re, sys

files=['~/Library/Application Support/Sublime Text 3/Local/Session.sublime_session',
	'~/Library/Application Support/Sublime Text 3/Local/Auto Save Session.sublime_session',
	'~/Library/Application Support/Sublime Text 2/Settings/Session.sublime_session',
	'~/Library/Application Support/Sublime Text 2/Settings/Auto Save Session.sublime_session',]

search = u'{query}'

def errorout():
	error=alfred.Item({'arg':''},'Open Sublime Text','No workspaces found')
	xml = alfred.xml([error])
	alfred.write(xml)

expr = re.compile("\"(.*%s.*\.sublime-workspace)\"" % search)
recentworkspaces = re.compile(".*recent_workspaces\":.*")
data=[]

for x in files:
	p=os.path.expanduser(x)
	if os.path.exists(p):
		recent=False
		with codecs.open(p,mode='r',encoding='utf-8') as f:
			for line in f:
				if recentworkspaces.match(line):
					recent=True
					continue
				if not recent:
					continue
				srch = expr.search(line)		
				if srch!= None and os.path.exists(srch.group(1)):
					data.append(srch.group(1))
	

if len(data) <= 0:
	errorout()
else:
	matches=[]
	for x in set(data): # removes duplication
		proj=os.path.basename(x)
		pt = os.path.expanduser(x)
		i = alfred.Item({'arg':pt},proj,'Open %s' % x)
		matches.append(i)
	xml = alfred.xml(matches)
	alfred.write(xml)



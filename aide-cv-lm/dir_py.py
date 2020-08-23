#! python2
#-*- encoding: utf-8 -*-

import os
import fnmatch

MYPATH = os.path.dirname(os.path.abspath(__file__))

def get_filelist(root, patterns='*', single_level=False, yield_folders=False):
	""" List files and directories """

	patterns = patterns.split(';')
	for path, subdirs, files in os.walk(root):
		if yield_folders:
			files.extend(subdirs)
		files.sort()
		for name in files:
			for pattern in patterns:
				if fnmatch.fnmatch(name, pattern):
					yield os.path.join(path, name)
					break
		if single_level:
			break


def main():

	data = []
	tups = []
	tmp = [x for x in get_filelist(MYPATH, patterns='*', single_level=False, yield_folders=True)]
	flist = [x for x in get_filelist(MYPATH, patterns='*', single_level=False, yield_folders=True)]

	dlist = []
	for x in flist:
		if os.path.isdir(x) and x not in dlist:
			dlist.append(x)

	res = []
	data = []
	for d in dlist:
		isRep1 = os.path.isfile(os.path.join(d, "reponse.pdf"))
		isRep2 = os.path.isfile(os.path.join(d, "reponse.txt"))
		isRep3 = os.path.isfile(os.path.join(d, "reponse.png"))
			
		isRepondu = '1' if isRep1 or isRep2 or isRep3 else ''
		
		t = "%s_%s" % (os.path.split(d)[-1], isRepondu)
		if t not in data and t.startswith("20"):
			data.append(t)



	with open('dir_py.txt', 'w') as flux:
		flux.write('\n'.join(data))
		flux.close()

	for d in data:
		date = d.split('_')[0]
		comp = d.split('_')[1].replace('-', ' ')
		ville= d.split('_')[2].replace('-', ' ')
		job  = d.split('_')[3].replace('-', ' ')
		rep  = d.split('_')[4]

		tups.append((comp, ville, date, job, rep))

	tups.sort()

	msg = ["DATE;CIE;VILLE;JOB;REPONDU;;;TOTAUX"]
	csv = []
	for i in range(len(tups)):
		tup = tups[i]
		comp  = tup[0]
		ville = tup[1]
		date  = tup[2]
		job   = tup[3]
		rep   = tup[4]
		print tup

		if i == 0:
			msg.append("{d};{c};{v};{j};{r};;CANDIDAT;=COUNTA(A2:A500)".format(d=date, c=comp, v=ville, j=job, r=rep))
		elif i == 1:
			msg.append("{d};{c};{v};{j};{r};;REPONSES;=SUM(E2:E500)".format(d=date, c=comp, v=ville, j=job, r=rep))
		elif i == 2:
			msg.append("{d};{c};{v};{j};{r};;TAUX REP;=TEXT(H3/H2,\"0 %\")".format(d=date, c=comp, v=ville, j=job, r=rep))
		else:
			msg.append("{d};{c};{v};{j};{r}".format(d=date, c=comp, v=ville, j=job, r=rep))


	with open('dir_py.csv', 'w') as f2:
		f2.write('\n'.join(msg))
		f2.close()




try:
	main()
except Exception as ex:
	print "ERREUR", ex
	with open('dir_py_ERR.log', 'w') as f:
		f.write("%s" % ex)
		f.close()
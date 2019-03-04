#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......red_python
#EXT.......py
#MAJOR....1
#MINOR....4
#DESCR....Remove Empty Dir python
#USAGE....red_v*.py 


def empties(root, patterns, debug=False, count=0, msg=[0]):
	listdir = list(get_filelist(root, patterns, single_level=False, yield_folders=True))
	for d in listdir:
		try:
			if not debug :
				os.rmdir(d)
				empties(root, patterns, debug, count+1)
			if debug :
				if not os.listdir(d):
					count += 1
		except:
			pass
	msg.append(count)
	return '--> %i dossiers vides supprimes' % (max(msg))
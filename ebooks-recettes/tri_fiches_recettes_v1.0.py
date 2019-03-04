#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......tri_fiches_recettes
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....parses fnames of recipes to classify them into 4 categories
#USAGE....tri_fiches_recettes.py


import os, shutil, fnmatch, time, sys

if os.name == "posix":
	SLASH = "/"
	DEST_FOLDER = "/media/reno/Playground/"
else:
	SLASH="\\"
	DEST_FOLDER = "F:\\"


MYPATH = os.path.dirname(os.path.abspath(__file__))
#MYPATH = 'F:\\LABO\\test-recette-db\\wdir'
SOURCE = 'F:\\EBOOKS-F1\\RECETTES\\FICHES\\'

if not os.path.isdir(SOURCE) : 
	sys.exit("Le chemin %s est introuvable" % SOURCE)


ext_search = '*.jpg;*.png;*.pdf'

##############################################

def get_filelist(root, patterns='*', single_level=False, yield_folders=False):
	'''
	List files and directories
		usage: lstdir = list(get_filelist(str_path, "*.jpg;*.png")
	'''
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


def read_file(file):
	'''
	lit un fichier donné

	'''
	flux=open(file,"r")
	data=flux.read()
	flux.close()

	return data


def fix_extensions_list(list_of_extensions):
	ext_fixed = []
	for ext in list_of_extensions:
		ext_fixed.append('*' + ext)
	return ext_fixed


def logging(log_file, msg, reset=False):
	if reset :
		if os.path.isfile(log_file):
			os.remove(log_file)
	flux = open(log_file, 'a')
	flux.write(msg)
	flux.write('\n')
	flux.close()


def anti_doublons(liste, sort=False):
	temp = []
	for element in liste:
		if element not in temp and element: 
			temp.append(element)
	if sort: temp.sort()
	return temp


def del_empty_dir(path):
	global rapport
	try:
		os.rmdir(path)
		rapport['Empties'].append(path)
		return 1
	except:
		return 0

###################################################

# get file list I
filelist = [ x for x in get_filelist(SOURCE, ext_search, single_level=True, yield_folders=False)]
#ignorelist = 'a la de d l les aux au . _ - \''.split(' ')
#sucrelist = 'gateau tarte pomme raisin'.split(' ')
#salelist = 'tomate fromage boeuf agneau poule poulet'.split(' ')
ignorelist = [ x.replace('\r', '').replace('\n', '') for x in open('ignore.lst', 'r') ]
ignorelist += ['. _ - \'']
sucrelist  = [ x.replace('\r', '').replace('\n', '') for x in open('sucre.lst', 'r') ]
salelist   = [ x.replace('\r', '').replace('\n', '') for x in open('sale.lst', 'r') ]

open('ignore.lst', 'w').write('\n'.join(anti_doublons(ignorelist, sort=True)))
open('sucre.lst' , 'w').write('\n'.join(anti_doublons(sucrelist,  sort=True)))
open('sale.lst'  , 'w').write('\n'.join(anti_doublons(salelist,   sort=True)))



#logging('log_%s.log' % NOW2, '%s\n%s\n' % (NOW2, len(NOW2)*'-'), True)
res = {}
ign = []
ign_mov = []
for f in filelist:
	fname = f.split(SLASH)[-1].replace('_', ' ').replace("'", ' ').split('.')[0].split(' ')
	res[f.split(SLASH)[-1]] = []
	for mot in fname:
		if mot.endswith('s') or mot.endswith('x'):
			mot = mot[:-1]
		if mot in sucrelist:
			res[f.split(SLASH)[-1]].append('sucre')
		if mot in salelist:
			res[f.split(SLASH)[-1]].append('sale')
		if mot not in sucrelist and mot not in salelist and mot not in ignorelist:
			ign.append('%s \t...\t %s' % (mot, ' '.join(fname)))
			res[f.split(SLASH)[-1]] = ['?']
			ign_mov.append('MOVE "%s" "%s"' % (f, f))
			continue


print 'ignore liste:'
print '\n'.join(ign)

open('unknowns.lst', 'w').write('\n'.join(anti_doublons(ign, sort=True)))
open('ign_move.txt', 'w').write('\n'.join(anti_doublons(ign_mov, sort=True)))

msg=[]
rob=[]
mov = (0,0)
for key in res.keys():
	msg.append('%s   %s' % (key, ' '.join(anti_doublons(res[key]))))
	if 'sale' in res[key]:
		mov = (key, 'sale_test\\%s' % key)
	if 'sucre' in res[key]:
		mov = (key, 'sucre_test\\%s' % key)
	if 'sucre' in res[key] and 'sale' in res[key]:
		mov = (key, 'sucre_sale_test\\%s' % key)
	if '?' in res[key] :
		mov = (key, 'unknown_test\\%s' % key)
	rob.append('ROBOCOPY "F:\\EBOOKS-F1\\RECETTES\\FICHES" "F:\\EBOOKS-F1\\RECETTES\\FICHES\\%s" "%s" /XO' % (mov[1].split('\\')[0], mov[0]))

open('robocop.bat', 'w').write('\n'.join(rob))


raw_input('pause')


open('resultat.txt', 'w').write('\n'.join(anti_doublons(msg, sort=True)))

#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......red
#EXT.......py
#MAJOR....2
#MINOR....1
#DESCR....Remove Empty Dir python
#USAGE....red_v*.py [ $DIR | usage | version ]

"""
NOTES DE VERSION
2017-09-21 v2.1   Minor fixes
2017-06-26 v2.0   Ajout de la prise de ldc (dir et option)
2017-06-26 v1.3   Simplification de la v1.1 ("rapport"?)
"""

import os, fnmatch
import sys, errno


usage   = "#USAGE....red_v*.py [ $DIR | usage | version ]"
version = "2.0"

SLASH = os.sep
MYPATH = os.path.dirname(os.path.abspath(__file__))

if len(sys.argv) > 1:
	option = sys.argv[1]
	if option.lower() == 'usage':
		sys.exit(usage)
	if option.lower() == 'version':
		sys.exit("#VERSION..red_v%s" % version)
	if not os.path.isdir(option):
		sys.exit("%s n'est ni un répertoire; ni une option.\n%s" % (option, usage))
else:
	option = MYPATH





def del_empty_dirs(s_dir):
	'''
	supprime les dossiers vides

	'''
	b_empty = True
	for s_target in os.listdir(s_dir):
		s_path = os.path.join(s_dir, s_target)
		if os.path.isdir(s_path):
			if not del_empty_dirs(s_path): b_empty = False
		else:
			b_empty = False
	if b_empty:
		#print('--- del: %s') % s_dir
		os.rmdir(s_dir)
		print('... %s | %s | %s') % ('@del_empty_dirs', s_dir, b_empty)
	return b_empty


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



def remove_empty_dirs_extended(path):
	''' EAFP Approach (Easier to Ask for Forgiveness than Permission) '''
	try:
		os.rmdir(path)
	except OSError as ex:
		# need import errno
		if ex.errno == errno.ENOTEMPTY:
			print "Dir not empty"


def remove_empty_dirs(path):
	''' EAFP Approach (Easier to Ask for Forgiveness than Permission) '''
	try:
		os.rmdir(path)
	except:
		pass


####################################################

filelist = [x for x in get_filelist(option, '*', single_level=False, yield_folders=True)]


count = 0
i = 0
while i < len(filelist):
	try:
		os.rmdir(filelist[i])
		count += 1
		i = 0
	except:
		i += 1

print('--> %i dossiers vides supprimés') % count
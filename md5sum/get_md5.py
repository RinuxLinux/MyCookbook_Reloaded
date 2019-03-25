#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......get_md5
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....retourne la checksum en md5 d'un fichier
#USAGE....get_md5_v*.py

import hashlib
import os
import fnmatch

if os.name == "posix":
	SLASH = "/"
else:
	SLASH = "\\"

MYPATH = os.path.dirname(os.path.abspath(__file__))
MYFILE = os.path.abspath(__file__)

#################################################

def md5(fname):
	'''
	import hashlib
	'''
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

#################################################
	
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

#################################################

md5 = md5(MYFILE)
#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......get_filelist
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....get file list (equiv dir)
#USAGE....filelist = list(get_filelist(MYPATH, '*.py;*.png', single_level=False, yield_folders=False)) => ['/path/to/file0', '/path/to/file1']

import os 
import fnmatch

MYPATH = os.path.dirname(os.path.abspath(__file__))
MYFILE = os.path.abspath(__file__)

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
			

filelist = list(get_filelist(MYPATH, '*.py;*.png', single_level=False, yield_folders=False))
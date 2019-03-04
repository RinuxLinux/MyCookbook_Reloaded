#! /usr/bin/python
#-*- coding: UTF-8 -*-
#NOM......convert_crlf_to_lf
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....Converts from CRLF to LF.  Print names of changed files.
#USAGE....convert_crlf_to_lf.py [ --descr -d | --usage -u | --version -v | ... ]

MYFNAME   	= "convert_crlf_to_lf.py"
MYVERSION 	= "v1.0"
MYEXT		= ".py"
MYDESCR		= "Converts from CRLF to LF.  Print names of changed files."
MYUSAGE		= "$ python {fn}_{vn}{ext}".format(fn=MYFNAME,vn=MYVERSION,ext=MYEXT)

'''
NOTE DE VERSION --- PENSER A CHANGER  etc.
2017-10-13 v1.0   Creation  
'''

def crlf(filelist):
	'''
	@param import sys, os
	@arg filelist = list
	Replace CRLF with LF in argument files.  Print names of changed files.
	'''

	for filename in filelist:
		print('... Converting from CRLF to LF %s') % filename
		if os.path.isdir(filename):
			print filename, "Directory!"
			continue
		data = open(filename, "rb").read()
		if '\0' in data:
			print filename, "Binary!"
			continue
		newdata = data.replace("\r\n", "\n")
		if newdata != data:
			print filename
			f = open(filename, "wb")
			f.write(newdata)
			f.close()

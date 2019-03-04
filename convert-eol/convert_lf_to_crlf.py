#! /usr/bin/python
#-*- coding: UTF-8 -*-
#NOM......convert_lf_to_crlf
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....Converts from LF to CRLF.  Print names of changed files.
#USAGE....convert_lf_to_crlf.py [ --descr -d | --usage -u | --version -v | ... ]

MYFNAME   	= "convert_lf_to_crlf.py"
MYVERSION 	= "v1.0"
MYEXT		= ".py"
MYDESCR		= "Replace LF with CRLF in argument files.  Print names of changed files."
MYUSAGE		= "$ python {fn}_{vn}{ext}".format(fn=MYFNAME,vn=MYVERSION,ext=MYEXT)

'''
NOTE DE VERSION --- PENSER A CHANGER  etc.
2017-10-13 v1.0   Creation  
'''

import sys, re, os

def lfcr(filelist):
	'''
	@param : import sys, re, os
	Replace LF with CRLF in argument files.  Print names of changed files.
	'''

	for filename in filelist:
		print('... Converting from LF to CRLF %s') % filename
		if os.path.isdir(filename):
			print filename, "Directory!"
			continue
		data = open(filename, "rb").read()
		if '\0' in data:
			print filename, "Binary!"
			continue
		newdata = re.sub("\r?\n", "\r\n", data)
		if newdata != data:
			print filename
			f = open(filename, "wb")
			f.write(newdata)
			f.close()



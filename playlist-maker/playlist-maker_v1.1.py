#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......playlist-maker
#EXT.......py
#MAJOR....1
#MINOR....1
#DESCR....make m3u playlists out of ['mkv', '.mp4', '.avi', '.ts'] found in F:\\DL\\Mouh-x
#USAGE....playlist-maker_v*.py 

MYPATH = "F:\\DL\\Mouh-x"
TOUT = ['mkv', '.mp4', '.avi', '.ts']

MYFNAME   	= "playlist-maker"
MYVERSION 	= "v1.1"
MYEXT		= ".py"
MYDESCR		= "make m3u playlists out of %s found in %s " % (TOUT, MYPATH)
MYUSAGE		= "$ python {fn}_{vn}{ext}".format(fn=MYFNAME,vn=MYVERSION,ext=MYEXT)

'''
NOTE DE VERSION --- PENSER A CHANGER $MYFNAME etc.
2017-08-25 v1.1   En-tête mise aux normes
'''

import glob, os, shutil


dir = []

def mydir(path):
	global TOUT, MYPATH
	flux = open('playlist.m3u', 'w')
	for root, dirs, files in os.walk(MYPATH):
		for file in files:
			for t in TOUT:
				#print 'file :', file
				if file.endswith(t):
					flux.write('#EXTINF:-1,' + file + '\n' + os.path.join(root, file) + '\n')
	flux.close()


mydir(MYPATH)

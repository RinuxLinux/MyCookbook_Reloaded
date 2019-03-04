#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......get_filesize_humanized
#EXT.......py
#MAJOR....1
#MINOR....1
#DESCR....get file size
#USAGE....GetHumanReadable(size,precision=2) => str(float)

import os

def getSize(filename):
	st = os.stat(filename)
	return st.st_size

def get_size(filename):
	return os.path.getsize(filename)
	
	
def GetHumanReadable(size,precision=2):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f %s"%(precision,size,suffixes[suffixIndex])
	

	
file = 'test_getsize.txt'

with open(file, 'w') as flux:
	flux.write('%s' % ('x' * 2**18)) 
	flux.close()

file2 = "F:\\MAGASIN-F1\\FILMS-F2\\PASSENGERS (2016)\\Passengers.2016.1080p.HC.HDRip.XviD.AC3-EVO.mkv"

tmp = []
tmp += [file, file2]


for file in tmp:
	print('Taille du fichier   : %s') % file
	print('avec os.stat        : %s') % GetHumanReadable(getSize(file), 2)
	print('avec os.path.getsize: %s') % GetHumanReadable(get_size(file), 2)
	
	
'''
OUTPUT
------
Taille du fichier   : test_getsize.txt
avec os.stat        : 256.00 KB
avec os.path.getsize: 256.00 KB
Taille du fichier   : F:\MAGASIN-F1\FILMS-F2\PASSENGERS (2016)\Passengers.2016.1080p.HC.HDRip.XviD.AC3-EVO.mkv
avec os.stat        : 3.79 GB
avec os.path.getsize: 3.79 GB
'''
#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......get_filesize_humanized
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....Return a humanized string representation of a number of bytes
#USAGE....humanize_bytes(bytes, precision=2) => str(float)

from __future__ import division
import doctest
import os

def humanize_bytes(bytes, precision=1):
    """
	Return a humanized string representation of a number of bytes.
    Assumes `from __future__ import division`.
    """
    abbrevs = (
        (1<<50L, 'PB'),
        (1<<40L, 'TB'),
        (1<<30L, 'GB'),
        (1<<20L, 'MB'),
        (1<<10L, 'KB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)
	
def getSize(filename):
	st = os.stat(filename)
	return st.st_size

def get_size(filename):
	return os.path.getsize(filename)

	
	
###########
# TESTING #
###########
file = 'test_getsize.txt'

with open(file, 'w') as flux:
	flux.write('%s' % ('x' * 2**18)) 
	flux.close()

tmp = [file]

for file in tmp:
	print('Taille du fichier   : %s') % file
	print('avec os.stat        : %s') % humanize_bytes(getSize(file), precision=2)
	print('avec os.path.getsize: %s') % humanize_bytes(get_size(file), precision=2)
	
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
#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......get_filesize
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....get file size
#USAGE....getSize(file) => float

import os

def getSize(filename):
	st = os.stat(filename)
	return st.st_size

def get_size(filename):
	return os.path.getsize(filename)
	
def get_human_readable(size):
	size = '10'
	units = ['B', 'KB', 'MB', 'GB', 'TB']
	i = 0
	while size/1024.**i >= 1 :
		i += 1
	print('%.2f%s') % (size/1024.**(i-1), units[i-1]) 
	'''	
	unit = 'B'
	if size/1024. >= 1:
		unit = 'KB'
		if size/(1024.**2) >= 1:
			unit = 'MB'
			if
			
	if 1e3  > filesize >= 1 : 
		return '%.2fKB' % (filesize/1e3)
	if 1e6  > filesize >= 1e3 : 
		return '%.2fMB' % (filesize/1e6)
	if 1e9  > filesize >= 1e6 : 
		return '%.2fGB' % (filesize/1e9)
	if filesize < 1:
		return '%.2fB' % size
	
	size = float(size)
	count = 0
	while size > 1:
		count += 1
		size = size / 1024.

	print('count: %i') % count
	#if count == -1: return '%.2f%s' % (size, 'B')
	if count == 2: return '%.2f%s' % (size, 'KB')
	if count == 3: return '%.2f%s' % (size, 'MB')
	if count == 4: return '%.2f%s' % (size, 'GB')
	'''
	return size


file = 'test_getsize.txt'

with open(file, 'w') as flux:
	flux.write('%s' % ('x' * 2**18)) 
	flux.close()

file2 = "F:\\MAGASIN-F1\\FILMS-F2\\PASSENGERS (2016)\\Passengers.2016.1080p.HC.HDRip.XviD.AC3-EVO.mkv"

tmp = []
tmp += [file, file2]

for file in tmp:
	print('Taille du fichier   : %s') % file
	print('avec os.stat        : %s') % get_human_readable(getSize(file))
	print('avec os.path.getsize: %s') % get_human_readable(get_size(file))
'''	
	count = 0
	t = get_human_readable(getSize(file))
	while t > 0:
		t = t / 1024
		print t, count
		count += 1

	if 1024 > count >= 0: print('%.2fB') % t
	if 10   > count >= 1024: print('%.2fKB') % t
	if 100  > count >= 10: print('%.2fMB') % t
	if 1000 > count >= 100: print('%.2fGB') % t
'''
	
'''
OUTPUT
Taille du fichier   : test_getsize.txt
avec os.stat        : 1.00Mb
avec os.path.getsize: 1.00Mb
Taille du fichier   : F:\MAGASIN-F1\FILMS-F2\PASSENGERS (2016)\Passengers.2016.1080p.HC.HDRip.XviD.AC3-EVO.mkv
avec os.stat        : 4.07Gb
avec os.path.getsize: 4.07Gb

Note: taille file2 est 3.78GB ou 3.97GB selon Win
'''



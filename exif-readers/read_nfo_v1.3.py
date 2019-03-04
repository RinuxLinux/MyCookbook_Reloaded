#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......read_nfo
#EXT.......py
#MAJOR....1
#MINOR....3
#DESCR....parse les nfo de photo
#USAGE....


'''
CHANGELOG:
	2017-07-07 v1.3   Adaptation photo
'''


import os, sys
import fnmatch, time


SLASH  = os.sep
NL     = os.linesep
MYPATH = os.path.dirname(os.path.abspath(__file__))
MYFILE = os.path.abspath(__file__)

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

def anti_doublons(liste, sort=False):
	'''
	tri les doublons et elimine les elements nuls
	'''
	print '--- --> Anti-doublons'
	temp = []
	for element in liste:
		if element not in temp and element: 
			temp.append(element)
	if sort: 
		temp.sort()
	return temp


def get_time():
	'''
	import time
	data   : [2017, 3, 27, 22, 15, 52, 0, 86, 1]
	return : sNow
	'''
	print '--- --> Get time'
	temps = [x for x in time.localtime()]
	yyyy  = '%04i' % temps[0]
	mm    = '%02i' % temps[1]
	dd    = '%02i' % temps[2]
	HH    = '%02i' % temps[3]
	MM    = '%02i' % temps[4]
	SS    = '%02i' % temps[5]
	return '%s-%s-%s_%s%s%s' % (yyyy,mm,dd,HH,MM,SS)

###################################################

NOW = get_time()

filelist = list(get_filelist(MYPATH, '*.nfo', single_level=True, yield_folders=False))
checklist_date = ['Media Create Date ', 'Create Date', 'Date/Time Original']


"""
File Name                       : 20161130_112837.jpg
File Modification Date/Time     : 2016:11:30 10:28:36+00:00
File Access Date/Time           : 2017:07:07 23:34:01+01:00
File Creation Date/Time         : 2017:07:07 23:34:01+01:00
Create Date                     : 2016:11:30 11:28:37.435
Date/Time Original              : 2016:11:30 11:28:37.435
Modify Date                     : 2016:11:30 11:28:37.435

File Type Extension             : jpg

Make                            : samsung
Camera Model Name               : SM-G900F

Image Width                     : 5312
Image Height                    : 2988
Image Size                      : 5312x2988
Exif Image Width                : 5312
Exif Image Height               : 2988




"""

final = {}
fin = []
fin2 = []

for file in filelist:
	final[file] = {}
	final[file]['date'] = []
	final[file]['file_ext'] = 'ext'
	final[file]['dimensions'] = 'WxH'
	final[file]['duration'] = 'duration'
	final[file]['filename'] = file.split(SLASH)[-1].replace('.nfo', '')
	final[file]['make'] = 'make'
	#final[file]['md5'] = hashfile(open(file, 'rb'), hashlib.md5())
	#final[file]['md5'] = md5(file)
	#final[file]['file_size'] = '0 MB'
	data0 = [x.replace('\n', '').replace('\r', '') for x in open(file, 'r')]

	for data in data0:
		# filename
		if data.startswith('File Name') : final[file]['filename'] = data[34:]

		# date & time
		for el in checklist_date:
			if data.startswith(el):
				datetaken = data[34:44].replace(':', '-')
				timetaken = data[45:].split('+')[0].replace(':', '')
				final[file]['date'].append('_'.join([datetaken, timetaken]))
				final[file]['date'] = anti_doublons(final[file]['date'])
				#if len(final[file]['date']) > 1 : print('%s') % sorted(final[file]['date'])[0]

		# image Size
		if data.startswith('Image Size') :
			final[file]['dimensions'] = data[34:]
		if 'image width' in data[:34].lower():
			final[file]['W'] = data[34:]
		if 'image height' in data[:34].lower():
			final[file]['H'] = data[34:]

		# make
		if data.startswith('Camera Model Name'):
			final[file]['make'] = data[34:]

		# file ext
		if data.startswith('File Type Extension'):
			final[file]['file_ext'] = data[34:]



for file in final.keys():
	# filename > date_size_make.ext   2016-06-06_185346_1920x1080_SM-G900F.jpg
	date = 'date'
	time = 'time'
	dim	     = final[file]['dimensions']
	make	 = final[file]['make']
	ext	     = final[file]['file_ext']
	filename = final[file]['filename'] 
	path	 = SLASH.join(file.split(SLASH)[:-1])

	# date & time
	target = sorted(final[file]['date'])
	i = 0
	while i < len(target):
		date_eval = eval(target[i].replace('-', '').replace('_', ''))
		if date_eval > 18e12:	# 1800-00-00_000000 <=> 18e12
			date = target[i].split('_')[0]
			time = target[i].split('_')[1]
			i = len(target)
		else :
			i += 1

	# dim
	if final[file]['dimensions']:
		dim = final[file]['dimensions']
	elif final[file]['W'] and final[file]['H']:
		dim = '%sx%s' % (final[file]['W'], final[file]['H'])


	#make
	if final[file]['make']:
		make = final[file]['make']

	# ext
	if final[file]['file_ext']:
		ext = final[file]['file_ext']

	newname = "%s_%s_%s_%s.%s" % (date, time, dim, make, ext)

	if date != 'date' or time != 'time' :
		fin.append('move "%s" %s\n' % (file.replace('.nfo', ''), newname))   # jpg
		fin.append('move "%s" %s\n' % (file, newname + '.nfo'))              # nfo
		fin2.append("%s;%s;%06i;%s;%s;%s;%s" % (\
			filename, \
			date,	 \
			int(time),	 \
			dim,	  \
			make,	 \
			ext,	  \
			newname ) )

	print('olfn = %s') % file
	print('newfn= %s.%s') % (newname, ext)
	print('date = %s') % date
	print('time = %s') % time
	print('dim  = %s') % dim
	print('make = %s') % make
	print('ext  = %s') % ext


fin.sort()
open('1_move_win.txt', 'w').write(''.join(fin))

	
'''
for file in *.mp4; do exiftool "$file" > "$file.nfo" ; echo "md5                             : $(echo $file | md5sum | sed 's/\ \ -//')" >> "$file".nfo; done
'''
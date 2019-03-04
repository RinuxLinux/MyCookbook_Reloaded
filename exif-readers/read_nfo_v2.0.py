#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......read_nfo
#EXT.......py
#MAJOR....2
#MINOR....0
#DESCR....parse les nfo de photo
#USAGE....


'''
CHANGELOG:
2017-07-08 v2.0   Reecriture (simplification)  
2017-07-07 v1.3   Adaptation photo
'''


import os, sys
import fnmatch, time
import EXIF

debug = False
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
	if debug : print '--- --> Anti-doublons'
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


flist = list(get_filelist(MYPATH, '*.nfo', single_level=True, yield_folders=False))

search_fname = ['File Name', 'Opening']
search_date  = ['Media Create Date ', 'Create Date', 'Date/Time Original', \
				'EXIF DateTimeOriginal (ASCII)', 'Image DateTime (ASCII)', \
				'EXIF DateTimeDigitized (ASCII)']
search_ext   = ['File Type Extension', 'Opening'] 
search_model = ['Camera Model Name', 'Image Model (ASCII)']
search_dim   = ['Image Size']

search_h = ['EXIF ExifImageLength (Long)','Image ImageLength (Long)', 'Exif Image Height']
search_w = ['EXIF ExifImageWidth (Long)', 'Image ImageWidth (Long)', 'Exif Image Width']

rename_template = 'date_dim_model.ext'

"""
POUR PLUS TARD (tabs not accurate)
	Image Make (ASCII)        : samsung
	Image Orientation (Short) : Rotated 90 CW
	Image XResolution (Ratio) : 72
	Image YResolution (Ratio) : 72
	EXIF ImageUniqueID (ASCII): F16QLHF01VB

Make                            : samsung
Orientation                     : Horizontal (normal)
X Resolution                    : 72
Y Resolution                    : 72
Image Unique ID                 : F16QLHF01VB

Exif Image Width                : 5312
Exif Image Height               : 2988

"""


catalog = {}
for file in flist:
	data = open(file, 'r').read().replace('\r', '').split('\n')
	#fname = file.split(SLASH)[-1]
	catalog[file] = {\
	'fname'   : [], \
	'date'    : [], \
	'ext'     : [], \
	'model'   : [], \
	'dim'     : [],
	'h' : [],
	'w': [] }

	for d in data:
		for f in search_fname:
			if d.lower().startswith(f.lower()):
				fname = d.split(': ')[-1].replace('\\', '$$$').replace('/', '$$$').split('$$$')[-1]
				catalog[file]['fname'].append(fname)
				
		for da in search_date:
			if d.lower().startswith(da.lower()):
				date = d.split(': ')[-1].split('.')[0]
				yyyy = date[:4]
				mm   = date[5:7]
				dd   = date[8:10]
				HHMMSS  = date[11:].replace(':', '') 
				date = '-'.join([yyyy, mm, dd]) + '_' + HHMMSS
				catalog[file]['date'].append(date)
				
		for se in search_ext:
			if d.lower().startswith(se.lower()):
				ext = d.split(': ')[-1].split('.')[-1]
				catalog[file]['ext'].append(ext)
				
		for sm in search_model:
			if d.lower().startswith(sm.lower()):
				model = d.split(': ')[-1]
				catalog[file]['model'].append(model)
				
		for sd in search_dim:
			if d.lower().startswith(sd.lower()):
				dim = d.split(': ')[-1]
				catalog[file]['dim'].append(dim)

		for w in search_w:
			if d.lower().startswith(w.lower()):
				wi = d.split(': ')[-1]
				catalog[file]['w'].append(wi)

		for h in search_h:
			if d.lower().startswith(h.lower()):
				hi = d.split(': ')[-1]
				catalog[file]['h'].append(hi)
				
rename_list = []
for key in catalog.keys():

	for k in catalog[key].keys():
		catalog[key][k] = anti_doublons(catalog[key][k])

		if len(catalog[key][k])   > 1 :
			print 'STOP', key, k, catalog[key]
		
	catalog[key]['dim'] = catalog[key]['w'][0] + "x" + catalog[key]['h'][0]

	print key
	
	date  = catalog[key]['date'][0]
	dim   = catalog[key]['dim']
	model = catalog[key]['model'][0]
	ext   = catalog[key]['ext'][0]

	newname = '%s_%s_%s.%s' % (date,dim,model,ext)

	if date or time :
		rename_list.append('move "%s" "%s"' % (key.replace('.nfo', ''), SLASH.join([MYPATH, 'test',newname])))   # jpg
		rename_list.append('move "%s" "%s"' % (key, SLASH.join([MYPATH, 'test',newname + '.nfo'])))              # nfo

open('results.bat', 'w').write('\n'.join(rename_list))

if not os.path.isdir(SLASH.join([MYPATH, 'test'])):
	os.makedirs(SLASH.join([MYPATH, 'test']))



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


	
'''
for file in *.mp4; do exiftool "$file" > "$file.nfo" ; echo "md5                             : $(echo $file | md5sum | sed 's/\ \ -//')" >> "$file".nfo; done







if len(catalog[key]['fname']) > 1 \
	or len(catalog[key]['date'])  > 1 \
	or len(catalog[key]['ext'])   > 1 \
	or len(catalog[key]['model']) > 1 \
	or len(catalog[key]['w']) > 1 \
	or len(catalog[key]['h']) > 1 \
	or len(catalog[key]['dim'])   > 1 :
		print 'STOP', key, catalog[key]
	else:
		catalog[key]['dim'] = catalog[key]['w'][0] + "x" + catalog[key]['h'][0]

	





'''
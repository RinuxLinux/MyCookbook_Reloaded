#!/usr/bin/env python
#-*- encoding: utf-8 -*-


############################################################
#### H E A D E R       #####################################
############################################################

MYFNAME   = "test_parse"
MYVERSION = "v1.2"
MYEXT	  = ".py"
MYDESCR	  = "Nouvelle version de parse_all"
MYUSAGE	  = "python test_parse.py"

# CHANGELOG
# ---------
# 2018-11-25 v1.2   Ajout de shows
# 2018-11-19 v1.1   Amelioration : une fonction par show
# 2018-11-19 v1.0   Premiere version optimisee pour Mini-Loup
# 2018-11-09 v0.2   Minor fixes



############################################################
#### S E T U P         #####################################
############################################################

import fnmatch
import os
import time
import re
import sys

#=============#
DEBUG  = False
DEBUG1 = False   # debug + detaillé
DEBUG2 = False   # utilisation de la vraie flist
DEBUG3 = False   # process normal mais sans move no mkdir
#DEBUG  = True
#=============#

if len(sys.argv) > 1:
	if sys.argv[1].upper() == 'DEBUG':
		DEBUG = True
	if sys.argv[1].upper() == 'DEBUG1':
		DEBUG  = True
		DEBUG1 = True
	if sys.argv[1].upper() == 'DEBUG2':
		DEBUG  = True
		DEBUG1 = True
		DEBUG2 = True
	if sys.argv[1].upper() == 'DEBUG3':
		DEBUG3 = True
	if sys.argv[1].upper() == 'VERSION':
		sys.exit("--> %s %s" % (MYFNAME, MYVERSION))
	if sys.argv[1].upper() == 'USAGE':
		msg = ["USAGE"]
		msg+= ["     $ python {mf}".format(mf=os.path.basename(MYFILE))]
		msg+= ["OPTIONS"]
		msg+= ["     'debug'     debuggage simple"]
		msg+= ["     'debug1'    debuggage détaillé"]
		msg+= ["     'debug2'    utilisation de la vraie flist"]
		msg+= ["     'debug3'    process normal mais sans move ni mkdir"]
		msg+= ["     'usage'     affiche ce message"]
		msg+= ["     'version'   affiche fname et version"]
		sys.exit("\n".join(msg))
 

NOW    = time.strftime("%Y-%m-%d_%H%M%S")
SLASH  = os.sep
NL     = os.linesep
MYPATH = os.path.dirname(os.path.abspath(__file__))
PARDIR = SLASH.join(MYPATH.split(SLASH)[:-1])
MYFILE = os.path.abspath(__file__)
AUTOEXEC = os.path.join(MYPATH, '%s_%s_autoexec.bat' % (MYFNAME, MYVERSION))
SETTINGS_DIR = os.path.join(MYPATH, "moutou-settings")


# where to find *.lst (config file and rename rules and what to keep, etc)
# CONFIG_FILE_RENAME_AND_MOVE
CFRAM_mouh   = os.path.join(SETTINGS_DIR, "list-move-mouh.lst")
CFRAM_series = os.path.join(SETTINGS_DIR, "list-move-mouh-series.lst")
CFRAM_films  = os.path.join(SETTINGS_DIR, "list-move-mouh-films.lst")
CFRAM_tv	 = os.path.join(SETTINGS_DIR, "list-move-mouh-tv.lst")
CFRAM_jan	 = os.path.join(SETTINGS_DIR, "list-move-mouh-jan.lst")

# DEST FOLDERS
if os.name == "posix":
	DEST_FOLDER = "/media/reno/Playground/"
	LVL0 = "-F"
	LVL1 = LVL0 + "1"
	LVL2 = LVL0 + "2"
else:
	DEST_FOLDER = "F:\\"
	LVL0 = "-F"
	LVL1 = LVL0 + "1"
	LVL2 = LVL0 + "2"

DEST_FOLDER_series   = os.path.join(DEST_FOLDER, "MAGASIN" + LVL1, "SERIES" + LVL2)
DEST_FOLDER_jan      = os.path.join(DEST_FOLDER_series, "JAN")
DEST_FOLDER_films	 = os.path.join(DEST_FOLDER, "MAGASIN" + LVL1, "FILMS"  + LVL2)
DEST_FOLDER_tv	     = os.path.join(DEST_FOLDER, "MAGASIN" + LVL1, "TV"	    + LVL2)
DEST_FOLDER_trailers = os.path.join(DEST_FOLDER, "MAGASIN" + LVL1, "TRAILERS" + LVL2)
DEST_FOLDER_ebooks   = os.path.join(DEST_FOLDER, "EBOOKS"  + LVL1)
DEST_FOLDER_mouh	 = os.path.join(DEST_FOLDER, "DL", "Mouh-x")

CALENDRIER = { \
	'janvier' : 1, 'fevrier': 2, 'février' : 2, 'f\xc3\xa9vrier' : 2, 'f\xe9vrier': 2,
	'mars' : 3, 'avril': 4, 'mai': 5, 'juin': 6, 'juillet': 7,
	'août': 8, 'ao\x96t': 8, 'septembre': 9, 'octobre': 10, 'novembre': 11,
	'décembre': 12, 'decembre': 12, 'd\xe9cembre': 12, 'd\xc3\xa9cembre': 12 }

HITLIST = [ \
	('&amp;', '&'),
	('\xc3\x89', 'E'),
	('\xc2\xb0', 'o'),
	('\xc3\xa9', 'e'),
	('\xc3\xa8', 'e'),
	('\xc3\xa0', 'a'),
	('\xb4', ''),
	('\x83', 'a'),
	('\xc9', 'E'),
	('\xb0', 'o'),
	('\xe8', 'e'),
	('\xe0', 'a'),
	('\xf4', 'o'),
	('\xe7', 'c'),
	('\xe9', 'e'),
	('\xea', 'e'),
	('\xf9', 'u'),
	('\x92', "."),
	('\xe2', 'a'),
	('{', '.'),
	('}', '.'),
	(' ', '.'),
	('-.', '.'),
	('.-', '.'),
	('.-.', '.'),
	('._.', '.'),
	(',', '.'),
	('..', '.'),
	("'", '.'),
	(' - ', '.'),
	('’', '.')]	

############################################################
#### C L A S S E S     #####################################
############################################################




############################################################
#### F O N C T I O N S #####################################
############################################################

def get_filelist(root, patterns='*', single_level=False, yield_folders=False):
	""" List files and directories """

	if DEBUG:
		print "[ GETFLST @0640 ] ... Getting file list in %s" % root

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

############################################################

def anti_doublons(liste, sort=False, case_sensitive=True):
	"""
	tri les doublons et elimine les elements nuls
	@arg ['liste', 'of', 'elements']
	@ret ['liste', 'sans', 'dups']
	"""

	if DEBUG1:
		print "[ ANTIDBL @0591 ] ... Anti-doublons, sort=%s, case_sensitive=%s" % (sort, case_sensitive)

	temp = []
	if case_sensitive:
		for element in liste:
			if element not in temp and element:
				temp.append(element)
	else:
		for element in liste:
			if element.lower() not in temp and element:
				temp.append(element)

	if sort:
		temp.sort()
	return temp

############################################################

def tee_autoexec(fullpath, mypath, myfn, myver, myfl):
	""" Creer le fichier .bat qui permet d'executer le script en loggant stderr/out """
	global MYPATH, MYFNAME, MYVERSION, NOW

	if DEBUG :
		print "[ AUTOEXE @0612 ] ... autoexec.bat, are you there ? %s" % os.path.isfile(fullpath)

	if not os.path.isfile(fullpath) and os.name == "nt":
		with open(fullpath, 'w') as f:
			f.write('REM {fn} {vn} {dt}'.format(fn=myfn,vn=myver,dt=NOW))
			f.write('REM cd /d "%s"\n' % mypath)
			f.write('{ff} 1> {fn}_{vn}_stdout.log 2> {fn}_{vn}_stderr.log\n'.format(ff=myfl,fn=myfn,vn=myver))
			f.close()

############################################################

def read_file(file, convert_EOL_to_LF=False, delete_EOL=False):
	""" 
	Read a file 
	Returns data as one string
	"""
	with open(file, 'r') as f:
		data = f.read()
		f.close()

	if delete_EOL:
		data = data.replace('\r\n', ' ')
		data = data.replace('\n', ' ')

	if convert_EOL_to_LF:
		data = data.replace('\r\n', '\n')

	return data

############################################################

def clean_fname_with_data_mouh(data_mouh, fname):
	""" Clean fname with data from data_mouh
	@arg : data_mouh => [('search', 'replacewith')]
	@arg : fname => 'Ma.Serie.S01E04.720p.mp4'
	@ret : new fname
	"""
	i=0
	while i < len(data_mouh) :	
		if data_mouh[i][0] in fname :
			fname = fname.replace(data_mouh[i][0], data_mouh[i][1])
			i = 0
		else :
			i += 1
	return fname

############################################################

def clean_fname_with_regex(fname):
	""" Clean fname with regex """

	# CLEAN DA FRANCE 4 (1)
	# _2018-10-22_1800_France 4_
	regex = r'[0-9-_]{10}[\s._]France[\s.]4[\s._]'
	fname = re.sub(regex, '', fname, flags=re.IGNORECASE)

	# CLEAN DA FRANCE X (1)
	# _France 4_2018_10_22_18_00
	regex = r'_France[\ _.-][0-9][\ _.-][0-9_]+\.txt'
	fname = re.sub(regex, '.txt', fname, flags=re.IGNORECASE)

	# CLEAN DA FRANCE X (2)
	# _France 4_2018_10_22_18_00
	regex = r'_France[\ _.-][0-9]_[0-9_]{0,12}\.txt'
	fname = re.sub(regex, '.txt', fname, flags=re.IGNORECASE)
	
	# CLEAN Arte
	# _Arte_2018_10_22_18_00
	regex = r'_Arte[\ _.-][0-9_]+.txt'
	fname = re.sub(regex, '.txt', fname, flags=re.IGNORECASE)

	# CLEAN Mini-Loup_
	fname = re.sub(r'mini-loup_', 'Mini-Loup.', fname, flags=re.IGNORECASE)

	# CLEAN HorribleSubs
	regex = r"(\[HorribleSubs\]\s)([\w\s]+)\sS(\d+)\D+(\d+)\s\[(\d{3,}p)\]"
	subst = "\\2.S\\3E\\4.\\5"
	fname = re.sub(regex, subst, fname, flags=re.IGNORECASE)

	# CLEAN S[0-9][-\ ._][0-9]+
	fname = re.sub(r"S(\d)(\E\d+)", "S0\\1\\2", fname, flags=re.IGNORECASE)

	# FIX Saison x Episode y
	regex = r"s(a|e)?(i|a)?s?o?n?[\ _\-.]?([0-9]+)([\ _\-.]+)?ep?i?s?o?d?e?([\ _\-.])?([0-9]+)"
	subst = "S\\3E\\6"
	fname = re.sub(regex, subst, fname, re.IGNORECASE)
	fname = re.sub(r"S([0-9])E([0-9])[^0-9]", "S0\\1E0\\2", fname, re.IGNORECASE)

	return fname

############################################################

def fix_season_episode(string):
	""" 
	Fix season & ep writing 
	
	@ver 20181011_0045
	@arg a string
	@ret a string
	"""
	if DEBUG:
		print("[ 0305 ] ... in  <-- %s" % string)
		
	#regex = r"(.+)(s|saison|season)?\s?(\d+)\s?Ep?i?s?o?d?e?\s?(\d+)(.+)"
	#regex = r"(.+)s(aison|eason)?[\.\ _]?(\d+)[\.\ _]?(e|é)p?i?s?o?d?e?\s?(\d+)\s?(.+)?"
	regex = r"(.+)s(aison|eason)?\s?(\d+)\s?(e|é)p?i?s?o?d?e?\s?(\d+)\s?(.+)"
	p = re.compile(regex, re.I)
	m = p.match(string)
	if m :
		debut = m.group(1).title()
		saison = "S%02i" % int(m.group(3))
		episode = "E%02i" % int( m.group(5))
		reste = m.group(6)
		string = "%s%s%s %s" % (debut, saison, episode, reste)

	if DEBUG :
		print("[ 0305 ] ... out --> %s" % string)

	return string

############################################################

def clean_fname_with_hitlist(fname) :
	""" Clean fname according to HITLIST bleow """

	# pour voir de quoi il s'agit :
	# print '\xc3\xa9'.decode('utf8')

	i = 0
	while i < len(HITLIST) :
		s = HITLIST[i][0]
		r = HITLIST[i][1]

		if s in fname :
			fname = fname.replace(s, r)
			i = 0
		else :
			i += 1

	return fname

############################################################

def get_showdir(start, Year=False):
	""" get new dirname
	fname => 'The.Goldbergs.2013.S04E06.720p.HDTV.x264-AVS.sub'
	start => 'The.Goldbergs.2013'
	@ret  => 'THE GOLDBERGS (2013)'
	"""

	tmpdname = start.replace('.', ' ').upper()
	tmpdname = tmpdname.replace('MARVELS', "MARVEL'S")
	tmpdname = tmpdname.replace('S.H.I.E.L.D', "S.H.I.E.L.D.")
	tmpdname = tmpdname.replace('THE LAST O.G', "THE LAST O.G.")
	tmpdname = tmpdname.replace('TOM CLANCYS', "TOM CLANCY'S")
	tmpdname = tmpdname.replace('THE HANDMAIDS TALE', "THE HANDMAID'S TALE")
	tmpdname = tmpdname.replace('THE HANDMAID S TALE', "THE HANDMAID'S TALE")
	tmpdname = tmpdname.replace('SI J ETAIS UN ANIMAL', "SI J'ETAIS UN ANIMAL")
	
	try:
		Year = int(tmpdname[-4:])
		Show = tmpdname[:-5]
		if Year < 1900 or Year > 2080 :
			Year = False
	except:
		#raise
		pass
		
	showdir = tmpdname.replace('_', ' - ') if not Year else '%s (%s)' % (Show.replace('_', ' - '), Year)
	return showdir

############################################################

def get_new_path(basename, showlist):
	""" 
	Identifier les shows concernes

	@arg : showlist['series'] = ['The.Punisher', 'The.Good.Place']
	@arg : fname (base)
	@ret : showname, newpath
	"""

	for key in showlist.keys() :
		
		for show in showlist[key] :
		#	print key
		#	if k.startswith('K') :
		#		print "[ 0400 ] +++ ", clean_fname_with_hitlist(k.lower()), basename.lower()
		#	if clean_fname_with_hitlist(k.lower()) in basename.lower() and k:
			if show and basename.lower().startswith(clean_fname_with_hitlist(show.lower())):
				if key == 'tv':
					new_path = eval('DEST_FOLDER_%s' % key)
				else:
					new_path = os.path.join( eval('DEST_FOLDER_%s' % key), get_showdir(show) )
				return (show, new_path)
	return False

############################################################

def isShow(basename, showlist):
	""" 
	Checks if fname is show-related 
	
	@arg : fname
	@arg : data['series'] = ['The.Punisher', 'YOU']
	@ret : 'The.Punisher' or False 
	"""
	for key in showlist.keys() :
		
		for show in showlist[key] :
		#	print key
		#	if k.startswith('K') :
		#		print "[ 0400 ] +++ ", clean_fname_with_hitlist(k.lower()), basename.lower()
		#	if clean_fname_with_hitlist(k.lower()) in basename.lower() and k:
			if show and basename.lower().startswith(clean_fname_with_hitlist(show.lower())):
				if key == 'tv':
					new_path = eval('DEST_FOLDER_%s' % key)
				else:
					new_path = os.path.join( eval('DEST_FOLDER_%s' % key), get_showdir(show) )
				return (show, new_path)
	return False

############################################################

def write_file(file, data, isList=False):
	""" Write data into a file """

	if isList :
		data = '\n'.join(data)

	with open(file, 'w') as f:
		f.write(data)
		f.close()

############################################################


def write_tvshow_nfo(xml_file, details) :
	""" Write tvshow.nfo """

	showtitle = details['showtitle']
	max_season = details['max_season']
	max_episode = details['max_episode']
	show_plot = details['show_plot']
	outline = details['outline']
	tagline = details['tagline']
	annee = details['year']
	credits = details['credits']
	studio = details['studio']
	status = details['status']
	genres = details['genres']

	xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>']
	xml+= ['<tvshow>']
	xml+= ['    <showtitle>%s</showtitle>' % showtitle]
	xml+= ['    <season>%s</season>' % max_season]
	xml+= ['    <episode>%s</episode>' % max_episode]
	xml+= ['    <plot>%s</plot>' % show_plot]
	xml+= ['    <outline>%s</outline>' % outline]
	xml+= ['    <tagline>Mini-Loup !</tagline>']
	xml+= ['    <year>%s</year>' % annee]
	xml+= gtemp
	xml+= ['    <credits>%s</credits>' % credits]
	xml+= ['    <studio>%s</studio>' % studio]
	xml+= ['    <status>%s</status>' % status]
	xml+= ['</tvshow>']	

	if DEBUG : 
		print("[ 0561 ] ... Ecriture tvshow.xml")
		print("[ 0561 ] ... BEGIN -------------")
		print '\n'.join(xml)
		print("[ 0561 ] ... END ---------------")

	if not DEBUG :
		with open(xml_file, "w") as flux:
			flux.write("\n".join(xml))
			flux.close()

def write_tvshow_nfo_2(xml_file, dico) :
	""" Pour produire le nfo du show uniquement """
	
	if not os.path.isfile(xml_file) and flist_temp :
		gtemp = []
		for g in dico['genres']:
			gtemp.append('    <genre>%s</genre>' % g)
	
		xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>']
		xml+= ['<tvshow>']
		xml+= ['    <title>%s</title>'         % dico['title']]
		xml+= ['    <showtitle>%s</showtitle>' % dico['showtitle']]
		xml+= ['    <season>%s</season>'       % dico['max_season']]
		xml+= ['    <episode>%s</episode>'     % dico['max_episode']]
		xml+= ['    <plot>%s</plot>'           % dico['plot']]
		xml+= ['    <outline>%s</outline>'     % dico['outline']]
		xml+= ['    <tagline>%s</tagline>'     % dico['tagline']]
		xml+= ['    <year>%s</year>'           % dico['annee']]
		xml+= gtemp
		xml+= ['    <credits>%s</credits>'     % dico['credits']]
		xml+= ['    <studio>%s</studio>'       % dico['studio']]
		xml+= ['    <status>%s</status>'       % dico['status']]
		xml+= ['</tvshow>']	

		if DEBUG : 
			print("[ PARWRTV @3002 ] ... Ecriture de %s" % xml_file)
			print('\n'.join(xml))
		if not DEBUG :
			with open(xml_file, 'w') as flux:
				flux.write('\n'.join(xml))
				flux.close()
				

############################################################
#### M A I N S         #####################################
############################################################
	
def main():
	""" Test de nouveau parsing de txt """

	# Get file list (*.txt)
	flist = [x for x in get_filelist(MYPATH, "*.txt", single_level=False, yield_folders=False)]
	
	if DEBUG:
		print "[ .... ] ... Nb of txt files detected :", len(flist)
	
	if not flist :
		print "[ 0768 ] ... No file detected. The end."
		return

	# Get list of shows
	showlist = {}
	showlist['jan']    = read_file(CFRAM_jan,    convert_EOL_to_LF=True).split('\n')
	showlist['series'] = read_file(CFRAM_series, convert_EOL_to_LF=True).split('\n')
	showlist['films']  = read_file(CFRAM_films,  convert_EOL_to_LF=True).split('\n')
	showlist['tv']     = read_file(CFRAM_tv,     convert_EOL_to_LF=True).split('\n')

	# data_m    : one string    => "('search', 'replaceby')   # comment"
	# data_mouh : list of tuple => [('search', 'replaceby')]
	data_m = read_file(CFRAM_mouh, convert_EOL_to_LF=True).split('\n')
	data_mouh = []
	for d in data_m :
		data_mouh.append(eval(d))
	
	dico = {}
	dir_to_create = []
	txt_to_read   = []
	inconnus = []

	for f in flist:
		fname = os.path.split(f)[-1]
		vu = False
		if fname.lower().startswith('vu') and 'france.3' in fname.replace(' ','.').replace('_','.').lower():
			vu = True
		
		# Fix Saison
		print("[ 0555 ] ... Fix Season & Episode writing :")
		fname = fix_season_episode(fname)
				
		# Clean fname with REGEX
		if not vu:
			fname = clean_fname_with_regex(fname)
		
		# Clean with HITLIST
		if not vu:
			fname = clean_fname_with_hitlist(fname)
		
		# Clean fname with CFRAM_mouh.lst
		fname = clean_fname_with_data_mouh(data_mouh, fname)
		
		# ID the show
		show = isShow(fname, showlist)
		if show is False:
			inconnus.append(fname)
			continue
		else:
			fpath = show[1]
			show = show[0]
		
		# Get PATH and FNAME
		#show, fpath = get_new_path(fname, showlist)
				
		# Sort file to read and mkdirs
		if fpath :
			
			if vu:
				nfo_name = "%s.nfo" % os.path.splitext(fname)[0]
			else:
				nfo_name = "%s.nfo" % os.path.splitext(clean_fname_with_regex(fname))[0]
			
			isDIR = os.path.isdir(fpath)
			isNFO = os.path.isfile(os.path.join(fpath, nfo_name))
						
			if not isDIR:
				if fpath not in dir_to_create:
					dir_to_create.append(fpath)
				txt_to_read.append((show, f, os.path.join(fpath, nfo_name)))

			if isDIR and not isNFO :
				# txt_to_read : (txt to read, nfo to write)
				txt_to_read.append((show, f, os.path.join(fpath, nfo_name)))
		
	# Read files
	print "[ 0465 ] ... nbr show detectes : ", len(txt_to_read)
	#print "[ 0465 ] ... mkdir %s" % dir_to_create
	
	# show : 'Karambolage'
	# txt  : 'F:\DL\Mouh-x\Karambolage - Loustic.txt"
	# nfo  : 'F:\MAGASIN-F1\TV-F2\Karambolage.Loustic.nfo'
	for show, txt, nfo in txt_to_read :
		details = None
		if not os.path.isfile(nfo) :
			data = read_file(txt, convert_EOL_to_LF=True, delete_EOL=False)

			show = show.lower().replace('!', '')
			show = show.replace("'", '_')
			show = show.replace('?', '_')
			show = show.replace('.', '_')
			show = show.replace(' ', '_')
			show = show.replace('-', '_')
			show = show.replace(':', '_')
			while '__' in show:
				show = show.replace('__', '_')
			
			# Analyse file content and retrieve details of show
			try:
				details = eval("analyse_data_%s(data)" % show.lower())
				if details:
					xml = xml_maker_episode(details)

					# Making dir if necessary
					try:
						print "[ 0674 ] ... making dir %s" % os.path.split(nfo)[0]
						os.makedirs(os.path.split(nfo)[0])
					except:
						pass
					
					# Writing nfo file
					print "[ 0680 ] ... Writing xml"
					with open(nfo, 'w') as h:
						h.write('\n'.join(xml))
						h.close()
				else:
					print "[ 0685 ] ... pas d'info utile pour le show %s" % show.upper()
			except Exception as ex:
				print "[ 0687 ] ERR %s" % ex
				continue
	

############################################################			

def analyse_data_vu(data, details={}):
	print "[ 0655 ] ... Processing data for VU"

	genres = ['Info', 'Culture', 'Zapping']
	gtemp = []
	for g in genres:
		gtemp.append('    <genre>%s</genre>' % g)

	details['header'] = 'episodedetails'
	details['showtitle'] = 'Vu'
	details['max_season'] = ''
	details['max_episode'] = ''
	details['season'] = ''
	details['episode'] = ''
	details['show_plot'] = "Un regard impertinent et libre, orchestré par Patrick Menais et son équipe, sur le monde de l'image."
	details['outline'] = 'Zapping'
	details['tagline'] = 'Ex-Zapping'
	details['show_tagline'] = 'Ex-Zapping'
	details['annee'] = ''
	details['credits'] = 'Patrick Menais'
	details['studio'] = 'France 3'
	details['status'] = 'Continuing'
	details['genres'] = '\n'.join(gtemp)	
	details['runtime'] = ''
	
	data = data.split('\n')
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])

	# 0 Vu
	# 1 --
	# 2 Diffusé sur France 3 le samedi 19 janvier 2019 à 20:00 - Durée : 7 min
	# 3 Un regard impertinent et libre, orchestré par Patrick Menais et son équipe, sur le monde de l'image.
	
	regex = r"diffus.+ sur ([\w0-9\ +-.!:]+) le \w+ (\d+) (\w+) (\d+) .+ \d+:\d+ - dur.+e : (\d+\s?min|\d+\s?[heures]+\s?\d+\s?min)"
	p = re.compile(regex, re.I)
	
	for d in data :
		m = p.match(d)
		if m:
			ligne = d
			break
		
	details['studio'] = m.group(1) if m else ''
	details['aired'] = "%s-%02i-%02i" % ( m.group(4), CALENDRIER[m.group(3)], int(m.group(2)) ) if m else ''
	details['year'] = m.group(4) if m else ''
	details['duree'] = m.group(5) if m else ''
	
	details['title'] = 'Vu | %s' % details['aired']
		
	if m:
		details['runtime'] = int(details['duree'].replace('min', '').split('h')[0])
		if len(details['duree'].split('h')) > 1:
			details['runtime'] = int(details['duree'].split('h')[0]) * 60
			details['runtime'] += int(details['duree'].replace('min', '').split('h')[1])
	
	# 0 Vu
	# 1 --
	# 2 Diffusé sur France 3 le samedi 19 janvier 2019 à 20:00 - Durée : 7 min
	# 3 Un regard impertinent et libre, orchestré par Patrick Menais et son équipe, sur le monde de l'image.
		
	# Choper les PLOT
	details['plot'] = tmp[-1]
	
	details['newfn_sans_ext'] = 'Vu.%s' % details['aired']
	
	return details
			
def analyse_data_mini_loup(data, details={}) :
	print "[ 0640 ] ... Processing data for MINI-LOUP"

	genres = ['Jan', 'Anime', 'Zouzous']
	gtemp = []
	for g in genres:
		gtemp.append('    <genre>%s</genre>' % g)
	
	details['header'] = 'episodedetails'
	details['showtitle'] = 'Mini-Loup'
	details['max_season'] = 2
	details['max_episode'] = 160
	details['show_plot'] = 'Mini-Loup !!'
	details['outline'] = 'Mini-Loup !!'
	details['tagline'] = 'Mini-Loup !!'
	details['show_tagline'] = 'Mini-Loup !!'
	details['annee'] = 2018
	details['credits'] = 'Mini-Loup !!'
	details['studio'] = 'France 4'
	details['status'] = 'Continuing'
	details['genres'] = '\n'.join(gtemp)
	
	# 0 Mini-Loup - Saison 1 Épisode 28 - Crise de jalousie
	# 1 ---------------------------------------------------
	# 2 Crise de jalousie
	# 3 Diffusé sur France 4 le mardi 2 octobre 2018 à 12:10 - Durée : 7 min
	# 4 Mini-Loup trouve qu'Anicet est un peu trop collant. Vexé, Anicet se tourne vers Moussa afin de fabriquer un tableau végétal pour l'école. Mini-Loup a alors pour partenaire Napoléon, qui ne le ménage pas...
	data = data.split('\n')
	
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])

	# LIGNE 0 : saison, epidode et titre épisode
	ligne = tmp[0]
	
	details['season']  = ""
	details['episode'] = ""
	try:
		details['season']  = int(ligne.split(' - ')[1].split(' ')[1])
		details['episode'] = int(ligne.split(' - ')[1].split(' ')[3])
	except :
		pass
	
	titre_episode = ligne.split(' - ')[-1]
	details['title'] = ligne.split(' - ')[-1]
	
	# date0 : 28 Novembre 2017
	# date1 : 2017-11-28 (diffusion)
	# date2 : 11-28
	# date3 : 2017
	# diffusion: 2017-11-28 (date1)
	# runtime : 65
	ligne = tmp[3]
	
	## essai de tout choper sur une regex
	# duree  : 1h22min
	# runtime : 82
	regex = r"diffus.+ sur ([\w0-9\ +-.!:]+) le \w+ (\d+) (\w+) (\d+) .+ \d+:\d+ - dur.+e : (\d+\s?min|\d+\s?[heures]+\s?\d+\s?min)"
	p = re.compile(regex, re.I)
	
	studio = ''
	aired = ''
	year = ''
	duree = ''
	runtime = ''

	for d in data :
		m = p.match(ligne)
		if m:
			ligne = d
			break
		
	details['studio'] = m.group(1) if m else ""
	details['aired'] = "%s-%02i-%02i" % ( m.group(4), CALENDRIER[m.group(3)], int(m.group(2)) ) if m else ""
	details['year'] = m.group(4) if m else ""
	details['duree'] = m.group(5) if m else ""
	
	if m:
		runtime = int(details['duree'].replace('min', '').split('h')[0])
		if len(details['duree'].split('h')) > 1:
			runtime = int(details['duree'].split('h')[0]) * 60
			runtime += int(details['duree'].replace('min', '').split('h')[1])
		
	details['runtime'] = runtime
		
	# Choper les PLOT
	details['plot'] = "\n".join(tmp[4:])
	
	# tagline : Durée: duree\n* sous-titre1\n* sous-titre2
	if m :
		tagline = "%s - Durée : %s" % (details['title'], m.group(5))
	else :
		tagline = details['title']
	details['tagline'] = tagline

	return details

	
def analyse_data_karambolage(data, details={}):
	print "[ 0865 ] ... analyse pour karambolage"

	genres = ['Deutschland über alles', 'Linguistique']
	gtemp = []
	for g in genres:
		gtemp.append('    <genre>%s</genre>' % g)
	
	# 0 Karambolage - Bibendum / La Schufa
	# 1 ----------------------------------
	# 2 Diffusé sur Arte le dimanche 18 novembre 2018 à 20:36 - Durée : 12 min
	# 3 L’histoire de Bibendum / L’institution berlinoise : la Schufa / La devinette

	data = data.split('\n')
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])
	
	details['header'] = 'tvshow'
	details['title'] = ''
	details['showtitle'] = 'Karambolage'
	details['tagline'] = ''
	details['plot'] = ''
	details['aired'] = ''
	details['outline'] = ''
	details['runtime'] = ''
	details['genres'] = '\n'.join(gtemp)
	details['year'] = ''
	details['studio'] = 'Arte'
	details['season'] = ''
	details['episode'] = ''
	details['credits'] = ''
		
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])

	# 0 Karambolage - Bibendum / La Schufa
	# 1 ----------------------------------
	# 2 Diffusé sur Arte le dimanche 18 novembre 2018 à 20:36 - Durée : 12 min
	# 3 L’histoire de Bibendum / L’institution berlinoise : la Schufa / La devinette
	regex = r"diffus.+ sur ([\w0-9\ +-.!:]+) le \w+ (\d+) (\w+) (\d+) .+ \d+:\d+ - dur.+e : (\d+\s?min|\d+\s?[heures]+\s?\d+\s?min)"
	p = re.compile(regex, re.I)
	
	for d in data :
		m = p.match(d)
		if m:
			ligne = d
			break
		
	details['studio'] = m.group(1) if m else ''
	details['aired'] = "%s-%02i-%02i" % ( m.group(4), CALENDRIER[m.group(3)], int(m.group(2)) ) if m else ''
	details['year'] = m.group(4) if m else ''
	details['duree'] = m.group(5) if m else ''
	
	details['title'] = 'Karambolage | %s' % details['aired']
		
	if m:
		details['runtime'] = int(details['duree'].replace('min', '').split('h')[0])
		if len(details['duree'].split('h')) > 1:
			details['runtime'] = int(details['duree'].split('h')[0]) * 60
			details['runtime'] += int(details['duree'].replace('min', '').split('h')[1])
	
	# 0 Karambolage - Bibendum / La Schufa
	# 1 ----------------------------------
	# 2 Diffusé sur Arte le dimanche 18 novembre 2018 à 20:36 - Durée : 12 min
	# 3 L’histoire de Bibendum / L’institution berlinoise : la Schufa / La devinette	
	
	# Choper les PLOT
	details['plot'] = tmp[-1]
	
	# tagline : Durée: duree\n* sous-titre1\n* sous-titre2
	details['tagline'] = '* %s' % tmp[3].replace(' / ', '\n* ')
	
	return details

	
def analyse_data_zone_interdite(data, details={}):
	print "[ 0870 ] ... analyse pour zone_interdite"
    
	genres = ['Publicité', 'Société', 'Info', 'Culture']
	gtemp = []
	for g in genres:
		gtemp.append('    <genre>%s</genre>' % g)
	
	# 0 Zone interdite - En famille, ils construisent la maison de leurs rêves
	# 1 ----------------------------------------------------------------------
	# 2 Diffusé sur M6 le dimanche 18 novembre 2018 à 21:00 - Durée : 1 h 40
	# 3 Construire sa propre maison, c'e bla...
	# 4 À Montpellier (Hérault), Gaël et bla...
	# 5 En Haute-Savoie, Céline et blablabla...
	# 6 À côté de Lyon (Rhône), Xavier et bla..

	data = data.split('\n')
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])
	
	# <title>Zone Interdite [1-07] | Enfants de gitans : une vie de roi</title>
    # <showtitle>Zone Interdite</showtitle>
    # <outline>A vendre, pas cher</outline>
    # <tagline>Durée : 1h45min
	# Date  : 07 Janvier 2018</tagline>
    # <year>2018</year>
    # <runtime>105</runtime>
    # <thumb></thumb>
    # <credits>Mélissa machin</credits>

	details['header'] = 'tvshow'
	details['title'] = ''
	details['showtitle'] = 'Zone Interdite'
	details['tagline'] = ''
	details['plot'] = ''
	details['aired'] = ''
	details['outline'] = 'A vendre, pas cher'
	details['runtime'] = ''
	details['genres'] = '\n'.join(gtemp)
	details['year'] = ''
	details['studio'] = 'M6'
	details['season'] = ''
	details['episode'] = ''
	details['credits'] = 'Mélissa Machin'
		
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])

	# 0 Zone interdite - En famille, ils construisent la maison de leurs rêves
	# 1 ----------------------------------------------------------------------
	# 2 Diffusé sur M6 le dimanche 18 novembre 2018 à 21:00 - Durée : 1 h 40
	# 3 Construire sa propre maison, c'e bla...
	# 4 À Montpellier (Hérault), Gaël et bla...
	# 5 En Haute-Savoie, Céline et blablabla...
	# 6 À côté de Lyon (Rhône), Xavier et bla..
	
	regex = r"diffus.+ sur ([\w0-9\ +-.!:]+) le \w+ (\d+) (\w+) (\d+) .+ \d+:\d+ - dur.+e : ([0-9]+)\ ?(min|h)?\ ?([0-9]+)?\ ?(min)?"
	p = re.compile(regex, re.I)
	
	for d in data :
		m = p.match(d)
		if m:
			ligne = d
			break

	if m:
		chaine = m.group(1)
		jour   = m.group(2)
		mois_l = m.group(3)
		annee  = m.group(4)
		tmps1 = m.group(5)
		unit1 = m.group(6)
		tmps2 = m.group(7)	
		unit2 = m.group(8)
		
		if unit1 == 'h':
			runtime = int(tmps1) * 60
		elif unit1 == 'min':
			runtime = int(tmps1)
			duree 
		else:
			runtime = 0

		if tmps2:
			duree = tmps1 + unit1 + tmps2
		else:
			duree = tmps1 + unit1

		if tmps2:
			runtime += int(tmps2)
		
	# <title>Zone Interdite [1-07] | Enfants de gitans : une vie de roi</title>
    # <showtitle>Zone Interdite</showtitle>
    # <outline>A vendre, pas cher</outline>
    # <tagline>Durée : 1h45min
	# Date  : 07 Janvier 2018</tagline>
    # <year>2018</year>
    # <runtime>105</runtime>
    # <thumb></thumb>
    # <credits>Mélissa machin</credits>
	
	details['studio']= chaine
	details['aired'] = "%s-%02i-%02i" % ( annee, CALENDRIER[mois_l], int(jour) ) if m else ''
	details['date']  = "%s %s %s" % (jour, mois_l, annee) if m else '?'
	details['year']  = annee if m else ''
	details['duree'] = duree if m else ''
	details['runtime'] = runtime if m else ''
	details['title'] = '%s %s | %s' % (details['showtitle'], details['aired'], data[0][17:])
		
	# Choper les PLOT
	details['plot'] = '\n'.join(tmp[3:])
	
	# <tagline>Durée : 1h45min
	# Date  : 07 Janvier 2018</tagline>
	details['tagline'] = 'Durée : %s\nDate : %s' % (details['duree'], details['date'])
	
	return details

	
def analyse_data_enquete_exclusive(data, details={}):
	print "[ 0944 ] ... analyse pour ENQUETE EXCLUSIVE"
    
	genres = ['Publicité', 'Prostitution', 'Info', 'Nanard chez les Narcos']
	gtemp = []
	for g in genres:
		gtemp.append('    <genre>%s</genre>' % g)
	
	# 0 Enquête exclusive - Tensions raciales aux USA : le retour des vieux démons
	# 1 --------------------------------------------------------------------------
	# 2 Diffusé sur M6 le dimanche 18 novembre 2018 à 23:10 - Durée : 1 h 14
	# 3 Aux États-Unis, les tensions ...
	# 4 Dans de nombreux états, surto...
	# 5 La présidence Obama achevée, ...
	# 6 Deux communautés, deux univers..

	data = data.split('\n')
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])
	
	# <title>Enquête exclusive 2018-11-18 | Tensions raciales aux USA : le retour des vieux démons</title>
    # <showtitle>Enquête exclusive</showtitle>
    # <outline>Nanard chez les prostiputes</outline>
    # <tagline>Durée : 1h45min
	# Date  : 07 Janvier 2018</tagline>
    # <year>2018</year>
    # <runtime>105</runtime>
    # <thumb></thumb>
    # <credits>Nanard de la Villardière</credits>

	details['header'] = 'tvshow'
	details['title'] = ''
	details['showtitle'] = 'Enquête Exclusive'
	details['tagline'] = 'Nanard chez les ...'
	details['plot'] = ''
	details['aired'] = ''
	details['outline'] = ''
	details['runtime'] = ''
	details['genres'] = '\n'.join(gtemp)
	details['year'] = ''
	details['studio'] = 'M6'
	details['season'] = ''
	details['episode'] = ''
	details['credits'] = 'Nanard de la Villardière'
		
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])

	# 0 Enquête exclusive - Tensions raciales aux USA : le retour des vieux démons
	# 1 --------------------------------------------------------------------------
	# 2 Diffusé sur M6 le dimanche 18 novembre 2018 à 23:10 - Durée : 1 h 14
	# 3 Aux États-Unis, les tensions ...
	# 4 Dans de nombreux états, surto...
	# 5 La présidence Obama achevée, ...
	# 6 Deux communautés, deux univers..
	
	regex = r"diffus.+ sur ([\w0-9\ +-.!:]+) le \w+ (\d+) (\w+) (\d+) .+ \d+:\d+ - dur.+e : ([0-9]+)\ ?(min|h)?\ ?([0-9]+)?\ ?(min)?"
	p = re.compile(regex, re.I)
	
	for d in data :
		m = p.match(d)
		if m:
			ligne = d
			break

	if m:
		chaine = m.group(1)
		jour   = m.group(2)
		mois_l = m.group(3)
		annee  = m.group(4)
		tmps1 = m.group(5)
		unit1 = m.group(6)
		tmps2 = m.group(7)	
		unit2 = m.group(8)
		
		if unit1 == 'h':
			runtime = int(tmps1) * 60
		elif unit1 == 'min':
			runtime = int(tmps1)
			duree 
		else:
			runtime = 0

		if tmps2:
			duree = tmps1 + unit1 + tmps2
		else:
			duree = tmps1 + unit1

		if tmps2:
			runtime += int(tmps2)
		
	# <title>Enquête exclusive 2018-11-18 | Tensions raciales aux USA : le retour des vieux démons</title>
    # <showtitle>Enquête exclusive</showtitle>
    # <outline>Nanard chez les prostiputes</outline>
    # <tagline>Durée : 1h45min
	# Date  : 07 Janvier 2018</tagline>
    # <year>2018</year>
    # <runtime>105</runtime>
    # <thumb></thumb>
    # <credits>Nanard de la Villardière</credits>
	
	details['studio']= chaine
	details['aired'] = "%s-%02i-%02i" % ( annee, CALENDRIER[mois_l], int(jour) ) if m else ''
	details['date']  = "%s %s %s" % (jour, mois_l, annee) if m else '?'
	details['year']  = annee if m else ''
	details['duree'] = duree if m else ''
	details['runtime'] = runtime if m else ''
	details['title'] = '%s %s | %s' % (details['showtitle'], details['aired'], data[0][17:])
		
	# Choper les PLOT
	details['plot'] = data[0].split(' - ')[-1]
	
	# <tagline>Durée : 1h45min
	# Date  : 07 Janvier 2018</tagline>
	details['tagline'] = 'Durée : %s\nDate : %s' % (details['duree'], details['date'])
	
	return details
	
	
def analyse_data_si_j_etais_un_animal(data, details={}):
	print "[ 0993 ] ... Processing data for SI J'ETAIS UN ANIMAL"
		
	genres = ['Jan', 'Animaux', 'Zouzous']
	gtemp = []
	for g in genres:
		gtemp.append('    <genre>%s</genre>' % g)
	
	data = data.split('\n')
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])
			
	# 0 Si j'étais un animal - Si j'étais un hérisson
	# 1 ---------------------------------------------
	# 2 Si j'étais un hérisson
	# 3 Diffusé sur France 4 le mardi 16 octobre 2018 à 13:25 - Durée : 6 min
	# 4 Annick la hérissonne se met à la recherche d'un repaire pour faire son nid et accueillir ses petits.

	regex = r"diffus.+ sur ([\w0-9\ +-.!:]+) le \w+ (\d+) (\w+) (\d+) .+ \d+:\d+ - dur.+e : ([0-9]+)\ ?(min|h)?\ ?([0-9]+)?\ ?(min)?"
	p = re.compile(regex, re.I)
	
	for d in data :
		m = p.match(d)
		if m:
			ligne = d
			break

	if m:
		chaine = m.group(1)
		jour   = m.group(2)
		mois_l = m.group(3)
		annee  = m.group(4)
		tmps1 = m.group(5)
		unit1 = m.group(6)
		tmps2 = m.group(7)	
		unit2 = m.group(8)
		
		if unit1 == 'h':
			runtime = int(tmps1) * 60
		elif unit1 == 'min':
			runtime = int(tmps1)
			duree 
		else:
			runtime = 0

		if tmps2:
			duree = tmps1 + unit1 + tmps2
		else:
			duree = tmps1 + unit1

		if tmps2:
			runtime += int(tmps2)
	else:
		chaine = ''
		jour = ''
		mois_l = ''
		annee = ''
		runtime = ''
		duree = ''
	
	# <?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
	# <episodedetails>
	# 	<showtitle>Si j'étais un animal</showtitle>
	#	<title>Le phacochère</title>
	#	<tagline></tagline>
	#	<outline></outline>
	#	<plot>Vingt-quatre heures dans la vie d'Albert ...</plot>
	# 	<runtime>6</runtime>
	# 	<genre></genre>
	#	<aired>2018-10-17</aired>
	#	<year>2018</year>
	# 	<studio>France 4</studio>
	# </episodedetails>	
	
	details['header'] = 'episodedetails'
	details['showtitle'] ="Si j'étais un animal"
	details['title'] = tmp[0].replace("Si j'étais un animal - ", '')
	details['tagline'] = ''
	details['outline'] = ''
	details['plot'] = tmp[-1]	
	details['runtime'] = runtime if m else ''
	details['genres'] = '\n'.join(gtemp)
	details['aired'] = "%s-%02i-%02i" % ( annee, CALENDRIER[mois_l], int(jour) ) if m else ''
	details['studio']= chaine
	details['date']  = "%s %s %s" % (jour, mois_l, annee) if m else '?'
	details['year']  = annee if m else ''
	details['duree'] = duree if m else ''
	details['season'] = ''
	details['episode'] = ''
	details['credits'] = ''
	
	return details
		

def analyse_data_simon(data, details={}):
	print "[ 0993 ] ... Processing data for SIMON"
		
	genres = ['Jan', 'Anime', 'Zouzous']
	gtemp = []
	for g in genres:
		gtemp.append('    <genre>%s</genre>' % g)
	
	data = data.split('\n')
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])
			
	# 0 Simon - Saison 1 Épisode 35 - Ah ! Les poux
	# 1 -------------------------------------------
	# 2 Ah ! Les poux
	# 3 Diffusé sur France 5 le mardi 6 novembre 2018 à 07:30 - Durée : 6 min
	# 4 Simon est le meilleur copain de Lou, jusqu'à ce qu'il ...

	regex = r"diffus.+ sur ([\w0-9\ +-.!:]+) le \w+ (\d+) (\w+) (\d+) .+ \d+:\d+ - dur.+e : ([0-9]+)\ ?(min|h)?\ ?([0-9]+)?\ ?(min)?"
	p = re.compile(regex, re.I)
	
	for d in data :
		m = p.match(d)
		if m:
			ligne = d
			break

	duree = ''
	chaine = ''
	annee = ''
	
	if m:
		chaine = m.group(1)
		jour   = m.group(2)
		mois_l = m.group(3)
		annee  = m.group(4)
		tmps1 = m.group(5)
		unit1 = m.group(6)
		tmps2 = m.group(7)	
		unit2 = m.group(8)
		
		if unit1 == 'h':
			runtime = int(tmps1) * 60
		elif unit1 == 'min':
			runtime = int(tmps1)
			duree 
		else:
			runtime = 0

		if tmps2:
			duree = tmps1 + unit1 + tmps2
		else:
			duree = tmps1 + unit1

		if tmps2:
			runtime += int(tmps2)

	# LIGNE 0 : saison, epidode et titre épisode
	ligne = tmp[0]
	
	details['season']  = ''
	details['episode'] = ''
	try:
		details['season']  = int(ligne.split(' - ')[1].split(' ')[1])
		details['episode'] = int(ligne.split(' - ')[1].split(' ')[3])
	except :
		pass
	
	# <?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
	# <episodedetails>
	# 	<showtitle>Simon</showtitle>
	#	<title>Ah ! Les poux</title>
	#	<tagline></tagline>
	#	<outline></outline>
	#	<season>1</season>
	#	<episode>35</episode>
	#	<plot>Simon est le meilleur copain de Lou, jusqu'à ce qu'il ...</plot>
	# 	<runtime>6</runtime>
	# 	<genre></genre>
	#	<aired>2018-11-06</aired>
	#	<year>2018</year>
	# 	<studio>France 4</studio>
	# </episodedetails>	
	
	details['header'] = 'episodedetails'
	details['showtitle'] = 'Simon'
	# saison titre : details['title'] = tmp[0].replace("Si j'étais un animal - ", '')
	details['title'] = data[0].split(' - ')[-1]
	details['tagline'] = ''
	details['outline'] = ''
	details['plot'] = tmp[-1]	
	details['runtime'] = runtime if m else ''
	details['genres'] = '\n'.join(gtemp)
	details['aired'] = "%s-%02i-%02i" % ( annee, CALENDRIER[mois_l], int(jour) ) if m else ''
	details['studio']= chaine
	details['date']  = "%s %s %s" % (jour, mois_l, annee) if m else '?'
	details['year']  = annee if m else ''
	details['duree'] = duree if m else ''
	#details['season'] = ''
	#details['episode'] = ''
	details['credits'] = ''
	
	return details
		

def analyse_data_drolement_betes(data, details={}):
	""" 
	2018-12-06 13:22
	"""
	print "[ 1280 ] ... Processing data for DROLEMENT BETES"
		
	genres = ['Jan', 'Animaux', 'Jeu']
	gtemp = []
	for g in genres:
		gtemp.append('    <genre>%s</genre>' % g)
	
	data = data.split('\n')
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])
			
	# 0 Drôlement bêtes : les animaux en questions
	# 1 ------------------------------------------
	# 2 Diffusé sur France 4 le mardi 6 novembre 2018 à 19:25 - Durée : 46 min
	# 3 Deux équipes de célébrités testent leurs connaissances sur les animaux en cinq manches. 
	
	regex = r"diffus.+ sur ([\w0-9\ +-.!:]+) le \w+ (\d+) (\w+) (\d+) .+ \d+:\d+ - dur.+e : ([0-9]+)\ ?(min|h)?\ ?([0-9]+)?\ ?(min)?"
	p = re.compile(regex, re.I)
	
	for d in data :
		m = p.match(d)
		if m:
			ligne = d
			break
	
	chaine = ''
	jour = ''
	mois_l = ''
	annee = ''
	runtime = ''
	duree = ''
	if m:
		chaine = m.group(1)
		jour   = m.group(2)
		mois_l = m.group(3)
		annee  = m.group(4)
		tmps1 = m.group(5)
		unit1 = m.group(6)
		tmps2 = m.group(7)	
		unit2 = m.group(8)
		
		if unit1 == 'h':
			runtime = int(tmps1) * 60
		elif unit1 == 'min':
			runtime = int(tmps1)
			duree 
		else:
			runtime = 0

		if tmps2:
			duree = tmps1 + unit1 + tmps2
		else:
			duree = tmps1 + unit1

		if tmps2:
			runtime += int(tmps2)
	
	# <?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
	# <episodedetails>
	# 	<showtitle>Drôlement bêtes</showtitle>
	#	<title>Les animaux en question</title>
	#	<tagline></tagline>
	#	<outline></outline>
	#	<plot>Deux équipes de célébrités testent...</plot>
	# 	<runtime>43</runtime>
	# 	<genre>...</genre>
	#	<aired>2018-10-17</aired>
	#	<year>2018</year>
	# 	<studio>France 4</studio>
	# </episodedetails>	
	
	details['header'] = 'episodedetails'
	details['showtitle'] ="Drôlement bêtes : les animaux en questions"
	details['aired'] = "%s-%02i-%02i" % ( annee, CALENDRIER[mois_l], int(jour) ) if m else ''
	details['date']  = "%s %s %s" % (jour, mois_l, annee) if m else '?'
	details['title'] = 'Emission du %s' % details['date']
	details['tagline'] = 'Yes We Can!'
	details['outline'] = ''
	details['plot'] = tmp[-1]	
	details['runtime'] = runtime
	details['genres'] = '\n'.join(gtemp)
	
	details['studio']= chaine
	details['year']  = annee
	details['duree'] = duree
	details['season'] = ''
	details['episode'] = ''
	details['credits'] = ''
	
	return details
		



def analyse_data_bob_le_bricoleur(data, details={}):
	""" 
	2019-01-07 18:28
	"""
	print "[ 1386 ] ... Processing data for BOB LE BRICOLEUR"
		
	genres = ['Jan', 'Anime', 'Camion']
	gtemp = []
	for g in genres:
		gtemp.append('    <genre>%s</genre>' % g)
	
	data = data.split('\n')
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])
			
	# 0 Bob le bricoleur - Bienvenue à l'hiver
	# 1 --------------------------------------
	# 2 Bienvenue à l'hiver
	# 3 Diffusé sur France 4 le lundi 7 janvier 2019 à 13:10 - Durée : 12 min
	# 4 Bob le bricoleur porte bien son nom. Il est ...
	
	regex = r"diffus.+ sur ([\w0-9\ +-.!:]+) le \w+ (\d+) (\w+) (\d+) .+ \d+:\d+ - dur.+e : ([0-9]+)\ ?(min|h)?\ ?([0-9]+)?\ ?(min)?"
	p = re.compile(regex, re.I)
	
	for d in data :
		m = p.match(d)
		if m:
			ligne = d
			break
	
	chaine = ''
	jour = ''
	mois_l = ''
	annee = ''
	runtime = ''
	duree = ''
	if m:
		chaine = m.group(1)
		jour   = m.group(2)
		mois_l = m.group(3)
		annee  = m.group(4)
		tmps1 = m.group(5)
		unit1 = m.group(6)
		tmps2 = m.group(7)	
		unit2 = m.group(8)
		
		if unit1 == 'h':
			runtime = int(tmps1) * 60
		elif unit1 == 'min':
			runtime = int(tmps1)
			duree 
		else:
			runtime = 0

		if tmps2:
			duree = tmps1 + unit1 + tmps2
		else:
			duree = tmps1 + unit1

		if tmps2:
			runtime += int(tmps2)
	
	# <?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
	# <episodedetails>
	# 	<showtitle>Bob le bricoleur</showtitle>
	#	<title>Bienvenue à l'hiver</title>
	#	<tagline></tagline>
	#	<outline></outline>
	#	<plot>Bob est ...</plot>
	# 	<runtime>12</runtime>
	# 	<genre>...</genre>
	#	<aired>2018-10-17</aired>
	#	<year>2018</year>
	# 	<studio>France 4</studio>
	# </episodedetails>	
	
	details['header'] = 'episodedetails'
	details['showtitle'] = "Bob le bricoleur"
	details['aired'] = "%s-%02i-%02i" % ( annee, CALENDRIER[mois_l], int(jour) ) if m else ''
	details['date']  = "%s %s %s" % (jour, mois_l, annee) if m else '?'
	details['title'] = data[0].split(' - ')[-1]
	details['tagline'] = ''
	details['outline'] = ''
	details['plot'] = tmp[-1]	
	details['runtime'] = runtime
	details['genres'] = '\n'.join(gtemp)
	
	details['studio']= chaine
	details['date']  = "%s %s %s" % (jour, mois_l, annee) if m else '?'
	details['year']  = annee
	details['duree'] = duree
	details['season'] = ''
	details['episode'] = ''
	details['credits'] = ''
	
	return details

		
def analyse_data_wallace_et_gromit(data, details={}):
	print "[ 1137 ] ... Processing data for WALLACE ET GROMIT"
		
	genres = ['Jan', 'Anime', 'Zouzous']
	gtemp = []
	for g in genres:
		gtemp.append('    <genre>%s</genre>' % g)
	
	data = data.split('\n')
	tmp = []
	for i in range(0, len(data)):
		if data[i]:
			tmp.append(data[i])
			
	# 0 Wallace & Gromit : rasé de près
	# 1 -------------------------------
	# 2 Diffusé sur France 4 le dimanche 21 octobre 2018 à 14:45 - Durée : 31 min
	# 3 L'ingénieux Wallace et son chien Gromit ont créé une entreprise ...

	regex = r"diffus.+ sur ([\w0-9\ +-.!:]+) le \w+ (\d+) (\w+) (\d+) .+ \d+:\d+ - dur.+e : ([0-9]+)\ ?(min|h)?\ ?([0-9]+)?\ ?(min)?"
	p = re.compile(regex, re.I)
	
	for d in data :
		m = p.match(d)
		if m:
			ligne = d
			break

	if m:
		chaine = m.group(1)
		jour   = m.group(2)
		mois_l = m.group(3)
		annee  = m.group(4)
		tmps1 = m.group(5)
		unit1 = m.group(6)
		tmps2 = m.group(7)	
		unit2 = m.group(8)
		
		if unit1 == 'h':
			runtime = int(tmps1) * 60
		elif unit1 == 'min':
			runtime = int(tmps1)
			duree 
		else:
			runtime = 0

		if tmps2:
			duree = tmps1 + unit1 + tmps2
		else:
			duree = tmps1 + unit1

		if tmps2:
			runtime += int(tmps2)
	else:
		chaine = ''
		jour = ''
		mois_l = ''
		annee = ''
		runtime = ''
		duree = ''
		
	# LIGNE 0 : saison, epidode et titre épisode
	# ligne = tmp[0]
	
	# details['season']  = ''
	# details['episode'] = ''
	# try:
		# details['season']  = int(ligne.split(' - ')[1].split(' ')[1])
		# details['episode'] = int(ligne.split(' - ')[1].split(' ')[3])
	# except :
		# pass
	
	# <?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
	# <episodedetails>
	# 	<showtitle>Wallace et Gromit</showtitle>
	#	<title>Rasé de près</title>
	#	<tagline></tagline>
	#	<outline></outline>
	#	<season></season>
	#	<episode></episode>
	#	<plot>L'ingénieux Wallace et son chien Gromit ont créé une entreprise ...</plot>
	# 	<runtime>31</runtime>
	# 	<genre></genre>
	#	<aired>2018-11-06</aired>
	#	<year>2018</year>
	# 	<studio>France 4</studio>
	# </episodedetails>	
	
	details['header'] = 'episodedetails'
	details['showtitle'] = 'Wallace et Gromit'
	details['title'] = data[0].replace(':', '-').split(' - ')[-1].capitalize()
	details['tagline'] = 'Crackers!'
	details['outline'] = ''
	details['plot'] = tmp[-1]	
	details['runtime'] = runtime if m else ''
	details['genres'] = '\n'.join(gtemp)
	details['aired'] = "%s-%02i-%02i" % ( annee, CALENDRIER[mois_l], int(jour) ) if m else ''
	details['studio']= chaine
	details['date']  = "%s %s %s" % (jour, mois_l, annee) if m else '?'
	details['year']  = annee if m else ''
	details['duree'] = duree if m else ''
	details['season'] = ''
	details['episode'] = ''
	details['credits'] = ''
	
	return details
		

		
############################################################		
	
def xml_maker_episode(details):
	""" Renvoie le xml a ecrire sous forme de list """

	xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>']
	xml+= ['<%s>' % details['header']]
	xml+= ['    <title>%s</title>' % details['title']]
	xml+= ['    <showtitle>%s</showtitle>' % details['showtitle']]
	xml+= ['    <plot>%s</plot>' % details['plot']]
	xml+= ['    <outline>%s</outline>' % details['outline'] ]
	xml+= ['    <tagline>%s</tagline>' % details['tagline'] ]
	xml+= ['    <season>%s</season>' % details['season'] ]
	xml+= ['    <episode>%s</episode>' % details['episode'] ]
	xml+= ['    <year>%s</year>' % details['year']]
	xml+= ['    <runtime>%s</runtime>' % details['runtime']]
	xml+= [details['genres']]
	xml+= ['    <credits>%s</credits>' % details['credits']]
	xml+= ['    <aired>%s</aired>' % details['aired']]
	xml+= ['    <studio>%s</studio>' % details['studio']]
	xml+= ['</%s>' % details['header']]
	
	if DEBUG:
		msg = "xml_maker debug for %s" % details['showtitle'].upper()
		print "[ 1100 ] ... %s" % msg
		print "[ 1100 ] vvv", 'v'*len(msg)
		print '\n'.join(xml)
		print "[ 1100 ] ^^^", '^'*len(msg)
	
	return xml

def analyse_data(data, details={}):
	""" Analyse data contenu dans txt """

	# 0 Mini-Loup - Saison 1 Épisode 28 - Crise de jalousie
	# 1 ---------------------------------------------------
	# 2 Crise de jalousie
	# 3 Diffusé sur France 4 le mardi 2 octobre 2018 à 12:10 - Durée : 7 min
	# 4 Mini-Loup trouve qu'Anicet est un peu trop collant. Vexé, Anicet se tourne vers Moussa afin de fabriquer un tableau végétal pour l'école. Mini-Loup a alors pour partenaire Napoléon, qui ne le ménage pas...

	# Saison, epidode et titre épisode
	regex = r"([a-z-\ ]+)( - )(saison\ )?([0-9]+)?( .+pisode )?([0-9]+)?( - )?(.+)"
	p = re.compile(regex, re.I)
	m = p.match(data)

	showtitle = m.group(1) if m else ''
	title = m.group(8) if m else ''
	season = ''
	episode = ''

	if m :
		try:
			season = "%02i" % int(m.group(4))
			episode = "%02i" % int(m.group(6))
		except:
			season = ''
			episode = ''

	# Chaine, date, duree
	regex = r"diffus. sur ([\w0-9\ +-.!:]+) le \w+ (\d+) (\w+) (\d+) . \d+:\d+ - dur.e : (\d+\s?min|\d+\s?[heures]+\s?\d+\s?min)"
	p = re.compile(regex, re.I)
		
	studio = ''
	aired = ''
	year = ''
	duree = ''
	runtime = ''

	for line in data.split('\n'):
		
		for s, r in HITLIST:
			line = line.replace(s,r)
		
		m = p.match(line)
		
		if m :
			studio =  m.group(1)
			aired = "%s-%02i-%02i" % ( m.group(4), CALENDRIER[m.group(3)], int(m.group(2)) )
			year = m.group(4)
			duree = m.group(5)
			runtime = int(duree.replace('min', '').split('h')[0])
			if len(duree.split('h')) > 1:
				runtime = int(duree.split('h')[0]) * 60
				runtime += int(duree.replace('min', '').split('h')[1])
			break

	# Plot
	plot = data.split('\n')[-1]

	# on met tout au meme endroit
	details['showtitle'] = showtitle
	details['title'] = title
	details['season'] = season
	details['episode'] = episode
	details['aired'] = aired
	details['year'] = year
	details['duree'] = duree
	details['runtime'] = runtime
	details['studio'] = studio
	details['plot'] = plot
	
	return details

	


main()







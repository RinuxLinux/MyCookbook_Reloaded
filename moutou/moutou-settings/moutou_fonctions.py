#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#NOM......moutou_fonction
#EXT.......py
#MAJOR....6
#MINOR....7
#DESCR....module comprenant toutes les fonctions necessaires a moutou
#USAGE....moutou_v*.py
MYFNAME_IN_MODULE 	= "moutou_fonctions"
MYVERSION_IN_MODULE = "v6.7"
MYEXT_IN_MODULE		= ".py"
MYDESCR_IN_MODULE	= "module comprenant toutes les fonctions necessaires a moutou"
MYUSAGE_IN_MODULE	= "sys.path.append(MYPATH + SLASH + 'moutou-settings')\nfrom moutou_fonctions import *"
"""
NOTE DE VERSION --- PENSER A CHANGER $MYFNAME_IN_MODULE etc.
2018-12-22 v6.7   fonction traitement special fname DROLEMENT BETE
2018-10-19 v6.6   Ajout de nouveaux parse pour futur nfo
2018-10-11 v6.5   regex / mini-loup / *.nfo
2018-09-24 v6.4   ajout de regex pour clean fname dans get_newfname(self, data_mouh)
2018-04-12 v6.3   ajout DEBUG3 : normal process but no move, no mkdir
2017-12-15 v6.2   Correction parse ENVOYE SPECIAL (new input)
2017-12-11 v6.1   New parse_zi()
2017-11-10 v6.0   Modularisation
2017-11-02 v5.2   Amelioration build_robocop(): meilleur output
2017-10-23 v5.1   Version nettoyée des fonctions superflues
2017-10-14 v5.0   Rajeunissement, Introduction des classes
2017-10-13 v4.24  Fix robocop factory
"""

##################################################################
#### S E T U P         ###########################################
##################################################################

import os, shutil, fnmatch, time, sys
import re
#import hashlib
#import sqlite3
try :
	import wmi
except :
	pass

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
		sys.exit("--> %s %s" % (MYFNAME_IN_MODULE, MYVERSION_IN_MODULE))
	if sys.argv[1].upper() == 'USAGE':
		msg = ["USAGE"]
		msg+= ["     $ python {mf}".format(mf=os.path.basename(MYFILE_IN_MODULE))]
		msg+= ["OPTIONS"]
		msg+= ["     'debug'     debuggage simple"]
		msg+= ["     'debug1'    debuggage détaillé"]
		msg+= ["     'debug2'    utilisation de la vraie flist"]
		msg+= ["     'debug3'    process normal mais sans move ni mkdir"]
		msg+= ["     'usage'     affiche ce message"]
		msg+= ["     'version'   affiche fname et version"]
		sys.exit("\n".join(msg))

		
##################################################################
#### G L O B A L E S   ###########################################
##################################################################		
		
		
NOW    = time.strftime("%Y-%m-%d_%H%M%S")
SLASH  = os.sep
NL     = os.linesep
MYPATH_IN_MODULE = os.path.dirname(os.path.abspath(__file__))
PARDIR_IN_MODULE = SLASH.join(MYPATH_IN_MODULE.split(SLASH)[:-1])
MYFILE_IN_MODULE = os.path.abspath(__file__)
AUTOEXEC_IN_MODULE = os.path.join(MYPATH_IN_MODULE, '%s_%s_autoexec.bat' % (MYFNAME_IN_MODULE, MYVERSION_IN_MODULE))


# set up subfolders for settings and eventual output
SUBFOLDER_settings = 'moutou-settings'
SUBFOLDER_output   = 'moutou-output'
FULLSUBSET = MYPATH_IN_MODULE


#for p in [FULLSUBSET, FullSubOut]:
#	if not os.path.isdir(p):
#		os.makedirs(p)

# INFO RELATIVE AU FICHIER init POUR LES starter A AJOUTER
ININAME = 'moutou_InsertNameHere.ini'
INIFILE = PARDIR_IN_MODULE + SLASH + ININAME
SECTIONS = ['TV', 'FILMS', 'SERIES', 'JAN']

# set up DEST_FOLDER according to OS
if os.name == "posix":
	DEST_FOLDER = "/media/reno/Playground/"
else:
	DEST_FOLDER = "F:\\"

# set up DEST_FOLDER for each category
LVL0 = "-F"
LVL1 = LVL0 + "1"
LVL2 = LVL0 + "2"

DEST_FOLDER_series   = DEST_FOLDER + "MAGASIN" + LVL1 + SLASH + "SERIES"   + LVL2
DEST_FOLDER_jan      = DEST_FOLDER_series + SLASH + "JAN"
DEST_FOLDER_films	 = DEST_FOLDER + "MAGASIN" + LVL1 + SLASH + "FILMS"	+ LVL2
DEST_FOLDER_tv	     = DEST_FOLDER + "MAGASIN" + LVL1 + SLASH + "TV"	   + LVL2
DEST_FOLDER_trailers = DEST_FOLDER + "MAGASIN" + LVL1 + SLASH + "TRAILERS" + LVL2
DEST_FOLDER_ebooks   = DEST_FOLDER + "EBOOKS"  + LVL1
DEST_FOLDER_mouh	 = DEST_FOLDER + "DL" + SLASH + "Mouh-x"

# where to find *.lst (config file and rename rules and what to keep, etc)
# CONFIG_FILE_RENAME_AND_MOVE
CFRAM_mouh   = SLASH.join([MYPATH_IN_MODULE, "list-move-mouh.lst"])
CFRAM_series = SLASH.join([MYPATH_IN_MODULE, "list-move-mouh-series.lst"])
CFRAM_films  = SLASH.join([MYPATH_IN_MODULE, "list-move-mouh-films.lst"])
CFRAM_tv	 = SLASH.join([MYPATH_IN_MODULE, "list-move-mouh-tv.lst"])
CFRAM_jan	 = SLASH.join([MYPATH_IN_MODULE, "list-move-mouh-jan.lst"])

# liste de faux fname a utiliser en cas de debug

FKEEP_DEBUG  = SLASH.join([MYPATH_IN_MODULE, "fkeep_debug.lst"])
FDEL_DEBUG   = SLASH.join([MYPATH_IN_MODULE, "fdel_debug.lst"])

# set up EXTENSIONS
EXT_DOC = ['.txt', '.nfo']
EXT_EBO = ['.pdf', '.cbr', '.cbz', '.epub', '.azw3']
EXT_EXTRA = ['sample*.mkv','sample*.avi','sample*.mp4']
EXT_NET = ['.net', '.url', '.lnk']
EXT_PIC = ['.png', '.jpg', '.bmp']
EXT_SUB = ['.srt', '.sub', '.idx', '.ass', '.ssa']
EXT_VID = ['.mkv', '.mp4', '.avi', '.ts', '.mov', '.mpeg', '.mpg']

# set KEYWORDS for TRAILERS
DATA_TRAILERS = ['trailer', 'promo', 'clip', 'teaser', 'featurette', 'bande-annonce']

# Fichiers a supprimer d'office:
ELEMENTS_DEL = ['sample-', 'sample.']
KILL_LIST = [\
    'RARBG.COM.mp4',
    'Bot.redecouverte.epub',
	"L.ecrivain.national_Joncour.Serge.epub",
	'L.ecrivain.national_Joncour.Serge.epub',
	"L'ecrivain national - Joncour,Serge.epub",
	'Cyclopes V2 #2 (of 4) (2006).pdf',
	'Cyclopes.V2.#2.(of.4).(2006).pdf',
	'Histoire_et_psychanalyse_entre_-_Michel_de_Certeau.epub']

# Elements INTERNE au fname pour le renommage de fichier
RENAME_INSIDE = [(' - ', '.'),
				 ('\xb4', ''),
				 ('wWw.Extreme-Down.Net', ''),
		 		 ('+', '.'),
				 ('?', ''),
				 ('&amp;', '&'),
				 ('\xc2\xb0', 'o'),
				 ('\xc3\xa9', 'e'),
				 ('’', '.'),
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
				 ('\x92', "'"),
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
		 		 ("'", '.')]

ELEMENTS_REN  = [	'[eztv]', '-DDLFR.ORG',
					'-zaphyra-telechargementz', 'www.telechargementz-streaming.com',
					'MyVideoLinks',  'MyVideoLink', 'MyVideo',
					'.MaChO@zone-telechargement.com', '@zone-telechargement.com',
					'_fr.downmagaz.com', '_downmagaz.com', '_do.az.com', '_fr.downmagaz.com',
					'wWw.Extreme-Down.Net']

RAPPORT = []

# SPECIAL POPO
LISTE_POPO = ['CHICAGO FIRE', 'THE BOLD TYPE', 'THIS IS US', 'YOUNGER', "SORRY FOR YOUR LOSS"]


# ANTI_POPO = [\
	 # 'KEVIN CAN WAIT', 'STAR TREK DISCOVERY','THE FLASH (2014)',
	 # 'MR ROBOT', 'DAMNATION', 'LETHAL WEAPON', "MARVEL'S THE PUNISHER",
     # "MARVEL'S IRON FIST", "MANIFEST", 
	 # 'EXTINCT (2017)', "THE BRIDGE (2011)", "TOM CLANCY'S JACK RYAN"]
	 
antipopo_file = os.path.join(MYPATH_IN_MODULE, 'antipopo.lst')
ANTI_POPO = []
with open(antipopo_file, 'r') as f:
	popotemp = f.read().upper()
	popotemp = popotemp.replace('\r', '\n')
	popotemp = popotemp.replace('\n\n', '\n')
	popotemp = popotemp.replace('.', ' ')
	popotemp = popotemp.replace('MARVELS', "MARVEL'S")
	popotemp = popotemp.replace('S H I E L D ', 'S.H.I.E.L.D.')
	popotemp = popotemp.split('\n')
	f.close()

for po in popotemp:
	if po and po not in ANTI_POPO:
		ANTI_POPO.append(po)

ANTI_POPO.sort()

with open(antipopo_file, 'w') as g:
	g.write('\n'.join(ANTI_POPO))
	g.write('\n')
	g.close()
	

LIST_DOUBLONS, LIST_MOVE, LIST_MKDIR, LIST_UNKNOWNS, LIST_DEL = [], [], [], [], []

##################################################################
#### C L A S S E S     ###########################################
##################################################################

class NewfileMaker:
	""" traiter chaque fichier comme un objet """
	def __init__(self, file):
		# catalog[file] = [oldpath, oldfname, newpath, showdir, newfname, isdir, isfile, flag, start]
		#                     0       1          2        3         4      5      6       7      8
		if DEBUG1:
			print "[ NFILMKR @0188 ] ... Initiate NewfileMaker instance :::", os.path.basename(file)

		self.oldfname = os.path.basename(file)
		self.oldpath  = os.path.dirname(file)
		self.oldfullname = file
		self.newfname = self.oldfname
		self.newpath  = self.oldpath
		self.showdir  = ''
		self.flag     = 'unk'
		self.start    = 'UNKNOWNS'
		self.showdir  = ''
		self.nfullpath = self.newpath
		self.nfullname = os.path.join(self.newpath, self.showdir, self.newfname)
		self.extension = os.path.splitext(file)[1]

	def ren_int(self, filename):
		""" 
		Renommage interne de filename
		
		@ver    20180924_1545
		@mod    import re
		@arg    old fname
		@ret    new fname
		"""
		if DEBUG1:
			print "[ NFMKRRI @0209 ] ... Newfilemaker rename inside fname :::", filename

		tups = RENAME_INSIDE
		i = 0
		while i < len(tups) :
			if tups[i][0] in filename:
				filename = filename.replace(tups[i][0], tups[i][1])
				i = 0
			else:
				i += 1

		self.newfname = filename
		return filename

	def new_fname(self, string, data):
		"""
		@descr     Nettoie fname dans son ensemble (pas que le debut)
		@self   => '/path/to/Z.N.306.720p.HDTV.x264-AVS.sub'
		@data   => [('Z.N.3', 'Z.Nation.S03E')]
		@ret    => 'Z.Nation.S03E06.720p.HDTV.x264-AVS.sub'
		@usage     newstring = string_cleaner(fname, data)
		"""

		count, i = 0, 0
		while i < len(data):
			search = string.lower().find(data[i][0].lower())

			if search != -1 and count < 20:
				upto = search + len(data[i][0])
				string = string[0:search] + data[i][1] + string[upto:]
				count += 1
				i = 0

			else:
				i += 1

		self.newfname = string
		return string

	def new_title(self, filename, max_season=99, episode_padding=2):
		""" Puts show titles in Proper Case and fix S01E23
		@args   old fname, max_season nbr, padding ep nbr
		@ret    new fname
		@note   "tre".find("e") => 2 ; "tre".find("z") => -1
		"""
		filename = filename.replace(' ', '.')
		filename = filename.replace('\t', '.')
		filename = filename.replace('..', '.')
		
		for i in range(0, max_season):
			season_search = "s%.*ie" % (episode_padding, i)  # todo: adapter pour ep-pad > 2
			if season_search in filename.lower():
				try:
					lookup = filename.lower().find(season_search) + len(season_search)
					part1 = filename[0:lookup].title()
					part2 = "%02i" % int(filename[lookup:].split('.')[0])
					part3 = '.'.join(filename[lookup:].split('.')[1:])
					filename = '%s%s.%s' % (part1, part2, part3)
					# part1 = filename[0:lookup].title()
					# part2 = filename[lookup:]
					# filename = '%s%s' % (part1, part2)
					if DEBUG:
						print "[ 0290 ] ************* ", filename
						#, part1, part2, saison1, filename
				except:
					print "[ 0338 ] ... new_title failed : %s" % filename
					pass

		self.newfname = filename
		return filename

	def get_newpath(self, nfname, data, flag):
		for d in data:
			if nfname.lower().startswith(d.lower()):
				self.flag = flag
				self.start = d
				return True
		return

	def get_showdir(self, fname, start, Year=False):
		""" get new dirname
		fname => 'The.Goldbergs.2013.S04E06.720p.HDTV.x264-AVS.sub'
		start => 'The.Goldbergs.2013'
		@ret  => 'THE GOLDBERGS 2013'
		"""
		tmpfname = fname.replace('.', ' ').upper().replace('MARVELS', "MARVEL'S")
		tmpdname = start.replace('.', ' ').upper().replace('MARVELS', "MARVEL'S")

		# exceptions, pask kodi est un peu con sur les bords
		if 'Marvels.Agents.of.S.H.I.E.L.D' in start:
			self.showdir = "MARVEL'S AGENTS OF S.H.I.E.L.D."

		elif 'Marvels.Inhumans' in start:
			self.showdir = "MARVEL'S INHUMANS"
			
		elif 'The.Last.O.G.' in start:
			self.showdir = "THE LAST O.G."
			
		elif 'si.j.etais.un.animal' in start.lower() :
			self.showdir = "SI J ETAIS UN ANIMAL"

		elif tmpfname.startswith(tmpdname):
			try:
				Year = int(tmpdname[-4:])
				Show = tmpdname[:-5]
				#print('%s (%s)') % (Show, Year)
				if Year < 1900 or Year > 2080 :
					Year = False
			except:
				#raise
				pass
			self.showdir = tmpdname.replace('_', ' - ') if not Year else '%s (%s)' % (Show.replace('_', ' - '), Year)

		else:
			self.showdir = tmpdname.replace('_', ' - ')

		return self.showdir

	def get_newfname(self, data_mouh):
		# CLEAN DA FRANCE 4
		regex = r'[0-9-_]{10}[\s._]France[\s.]4[\s._]'
		self.newfname = re.sub(regex, '', self.oldfname, flags=re.IGNORECASE)
		
		# CLEAN DA FRANCE x
		regex = r'[._]France[\ .][2345o][._][0-9-_]+\.'
		self.newfname = re.sub(regex, '.', self.newfname, flags=re.IGNORECASE)
		
		# CLEAN Saison ... Episode
		# regex = r'saison[.\ ]([0-9]+)[\ .]episode([0-9]+)'
		# self.newfname = re.sub(regex, 'S\\1E\\2', self.newfname, flags=re.IGNORECASE)
		
		self.newfname =  fix_season_episode(self.newfname)
		
		# CLEAN Saison ... Episode
		regex = r'saison[.\ ]([0-9]+)[\ .]episode([0-9]+)'
		self.newfname = re.sub(regex, 'S\\1E\\2', self.newfname, flags=re.IGNORECASE)
		
		# CLEAN Mini-Loup_
		self.newfname = re.sub(r'mini-loup_', 'Mini-Loup.', self.newfname, flags=re.IGNORECASE)
		
		# CLEAN HorribleSubs
		regex = r"(\[HorribleSubs\]\s)([\w\s]+)\sS(\d+)\D+(\d+)\s\[(\d{3,}p)\]"
		subst = "\\2.S\\3E\\4.\\5"
		self.newfname = re.sub(regex, subst, self.newfname, flags=re.IGNORECASE)
		self.newfname = re.sub(r"S(\d)(\E\d+)", "S0\\1\\2", self.newfname, flags=re.IGNORECASE)
		
		
		self.newfname = self.ren_int(self.newfname)
		self.newfname = self.new_fname(self.newfname, data_mouh)
		self.newfname = self.ren_int(self.newfname)
		self.newfname = self.new_title(self.newfname)
		return self.newfname

	def check_presence(self):
		self.isdir    = os.path.isdir(self.nfullpath)
		self.isfile   = os.path.isfile(self.nfullname)

	def get_action(self):
		global LIST_DOUBLONS, LIST_MOVE, LIST_MKDIR, LIST_UNKNOWNS

		if self.isfile and self.flag != 'unk' :
			LIST_DOUBLONS.append(self.oldfullname)

		if not self.isfile :
			LIST_MOVE.append((self.oldfullname, self.nfullname, self.flag))

		if not self.isdir and not self.isfile and self.nfullpath not in LIST_MKDIR:
			LIST_MKDIR.append(self.nfullpath)

		if self.flag == 'unk':
			LIST_UNKNOWNS.append(self.newfname)

	def detect_general(self, big_data):
		for tup in big_data:
			# tup = (flag, starter, dest_folder, showdir)
			flag = tup[0]
			starter = tup[1]

			if self.newfname.lower().startswith(starter.lower()):
				self.newpath = tup[2]
				self.showdir = tup[3] if flag != 'tv' else ''
				self.flag = flag
				self.nfullpath = SLASH.join(tup[2:4])
				self.nfullname = os.path.join(self.nfullpath, self.newfname)

	def detect_ebooks(self):
		if self.extension in EXT_EBO:
			self.nfullpath = DEST_FOLDER_ebooks
			self.nfullname = os.path.join(self.nfullpath, self.newfname)
			self.flag = 'ebo'

	def detect_trailers(self):
		for data in DATA_TRAILERS:
			if data.lower() in self.newfname.lower():
				self.nfullpath = DEST_FOLDER_trailers
				self.nfullname = os.path.join(self.nfullpath, self.newfname)
				self.flag = 'tra'

	def display_lists(self):
		print "*"*25
		for x in LIST_DOUBLONS:
			print "doublons ::: %s" % x
		for x in LIST_MKDIR:
			print "mkdir    ::: %s" % x
		for x, y, flag in LIST_MOVE:
			print "move %s ::: %s --> %s" % (flag, x, y)
		for x in LIST_DEL:
			print "DEL      ::: %s" % x
		for x in LIST_UNKNOWNS:
			print "unknowns ::: %s" % x


class ScriptMaker:
	"""build any script"""
	def __init__(self):
		if DEBUG1:
			print "[ SCRMKRI @0370 ] ... Initialisation instance ScriptMaker"
 		pass

	def writeScript(self, name, head=[], body=[], foot=[]):
		""" write the whole thing into scriptname """

		if DEBUG1:
			print "[ SCRMKRW @0377 ] ... Initiate script writer :::", name

		self.name  = name
		self.fname = os.path.basename(name)

		self.head = head
		self.body = body
		self.foot = foot

		if DEBUG1:
			print "[ SCRMKRW @0390 ] ... Writing ::: %s" % self.fname

		if self.head:
			whole = self.head
		else:
			sys.exit("[ SCRMKRW @0395 ] xxx ERROR empty header - There's nothing to write in %s !" % self.fname)

		if self.body:
			whole += self.body

		if self.foot:
			whole += self.foot

		with open(self.name, 'w') as f:
			f.write('\n'.join(whole))
			f.close()

	def readScript(self, name, anti_doublons=False, remove_eol=False, sort=False, replace_space_w_dot=False):
		""" returns data read, as list """

		self.name = name
		self.fname = os.path.basename(name)

		if DEBUG1:
			print "[ SCRMKRR @0407 ] ... Reading file :::", self.name

		self.data = [x for x in open(self.name, 'r')]

		if remove_eol:
			for i in range(0, len(self.data)):
				self.data[i] = self.data[i].replace('\r', '').replace('\n','')

		if replace_space_w_dot:
			for i in range(0, len(self.data)):
				self.data[i] = self.data[i].replace(' ','.')

		if sort:
			self.data.sort()

		if anti_doublons:
			tmp = []
			for d in self.data:
				if d and d not in tmp:
					tmp.append(d)

			self.data = tmp

		return self.data


class IniMaker(ScriptMaker):
	def __init__(self):
		""" Initialisation """

		if DEBUG1:
			print "[ --INI-- @0441 ] ... Initialisation instance"

		self.fpath = INIFILE
		self.fname = ININAME

		if not os.path.isfile(INIFILE):
			print "pass"

	def read_ini(self):
		"""
		lit fichier ini
		@param   inifile
		@return  ['data_ini']
		"""
		if DEBUG:
			print "[ READINI @0449 ] ... Reading ini file :::", INIFILE
		self.data_ini = self.readScript(INIFILE, anti_doublons=False, remove_eol=True, sort=False)

	def parse_ini(self):
		"""
		parse ini file
		@param   data_ini, SECTIONS
		@return  dict = { 'TV' : [], 'SERIES' : ['Zorro'], 'FILMS' : ['Proutman.2016', 'Proutman.2017'], 'JAN' : ['Shaun le mouton'] }
		"""
		if DEBUG1:
			print "[ PARSINI @0460 ] ... Parsing data from :::", ININAME

		self.parsed_data = {}

		tmp=[]
		for s in SECTIONS:
			try:
				tmp.append(self.data_ini.index('[%s]' % s))
			except ValueError as ex:
				print "[ PARSINI @0460 ] ... INI PARSING ERR :::", tmp, ex
				pass

		tmp.sort()

		i=0
		while i < len(self.data_ini):
			if i in tmp:
				key = self.data_ini[i].replace('[', '').replace(']', '')
				self.parsed_data[key] = []
			else:
				self.parsed_data[key].append(self.data_ini[i])
			i+=1

		for key in self.parsed_data.keys():
			tmp2 = []
			for d in self.parsed_data[key]:
				if d and d not in tmp2:
					tmp2.append(d.replace(' ', '.').title())

			self.parsed_data[key] = tmp2

	def update_lst(self):
		"""
		Write new data from ini into settings file
		@arg   dict = { 'TV' : [], 'SERIES' : ['Zorro'], 'FILMS' : ['Proutman.2016', 'Proutman.2017'], 'JAN' : ['Sam le pompier'] }
		@ret   None
		"""

		if DEBUG:
			print "[ UPDTINI @0497 ] ... Updating *.lst with ini content"

		for key in self.parsed_data.keys():
		
			if DEBUG2 : print "[ UPDTINI @0498 ] ... key of dict :", key

			self.new_data_trigger = False

			if self.parsed_data[key]:
				CFRAM = eval('CFRAM_%s' % key.lower())
				data_switch = self.readScript(CFRAM, anti_doublons=True, remove_eol=True, sort=True,  replace_space_w_dot=True)

				for el in self.parsed_data[key]:
					new_data = el.replace(" ", ".").title()
					if new_data not in data_switch:
						data_switch.append(new_data)
						self.new_data_trigger = True

				data_switch = anti_doublons(data_switch, sort=True, case_sensitive=False)

				if DEBUG or not self.new_data_trigger:
					plusplus = "***DEBUG IS ON*** %s" % (os.path.basename(CFRAM)) if DEBUG else "No new data to insert"
					print '[ UPDTINI @0523 ] ... Not updating lst :::', plusplus
				else:
					self.writeScript(CFRAM, data_switch)
					self.new_data_trigger = True

	def isIniDataInMainData(self):
		""" Check if data_ini well incorporated into main data """

		if DEBUG1:
			print "[ CHCKINI @0530 ] ... Check if ini content is now in data pool"

		self.IniDataIsInMainDataPool = True

		data1  = self.readScript(CFRAM_series)
		data1 += self.readScript(CFRAM_tv)
		data1 += self.readScript(CFRAM_films)
		data1  = anti_doublons(data1)

		data2 = self.parsed_data.values()

		tmp =[]
		for da in data2:
			if len(da) > 1:
				for d in da:
					if d and d not in tmp:
						tmp+=d
			else:
				if da and da not in tmp:
					tmp+=da
		data2 = tmp

		for d in data2:
			d = d.replace(' ', '.')
			if d not in data1:
				self.IniDataIsInMainDataPool = False

	def reset_ini(self):
		"""
		reset ini file
		"""
		if DEBUG:
			print "[ RSETINI @0561 ] ... Resetting", INIFILE

		header = '[TV]\n\n\n[SERIES]\n\n\n[FILMS]\n\n\n[JAN]\n\n\n'
		self.writeScript(INIFILE, [header])

	def iniProcess(self):
		""" equivalent de main_ini() """
		if DEBUG1:
			print '[ --INI-- @0436 ] ... BEGIN ini Processing'

		# => data_ini ['str']
		self.read_ini()
		# => parsed_data ['str']
		self.parse_ini()
		# update *.lst
		# => self.head, self.path, writeScript()
		self.update_lst()
		# => reset
		if self.new_data_trigger :
			self.reset_ini()
		self.reset_ini()

		if DEBUG1:
			print '[ --INI-- @0597 ] ... END ini Processing'


##################################################################
#### F O N C T I O N S ###########################################
##################################################################

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


##################################################################

def tee_autoexec(fullpath, mypath, myfn, myver, myfl):
	""" Creer le fichier .bat qui permet d'executer le script en loggant stderr/out """
	global MYPATH_IN_MODULE, MYFNAME_IN_MODULE, MYVERSION_IN_MODULE, NOW

	if DEBUG :
		print "[ AUTOEXE @0612 ] ... autoexec.bat, are you there ? %s" % os.path.isfile(fullpath)

	if not os.path.isfile(fullpath) and os.name == "nt":
		with open(fullpath, 'w') as f:
			f.write('REM {fn} {vn} {dt}'.format(fn=myfn,vn=myver,dt=NOW))
			f.write('REM cd /d "%s"\n' % mypath)
			f.write('{ff} 1> {fn}_{vn}_stdout.log 2> {fn}_{vn}_stderr.log\n'.format(ff=myfl,fn=myfn,vn=myver))
			f.close()

##################################################################

def get_extension(keep, delete):
	""" get extension list ready for get_flist() pattern """

	if DEBUG1:
		print "[ GET_EXT @0628 ] ... Getting extension list ready for get_flist() pattern"

	ext_keep = '*' + ';*'.join(keep)
	ext_DEL = '*' + ';*'.join(delete) +  ';RARBG.com.mp4'
	return ext_keep, ext_DEL

##################################################################

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

##################################################################

def parse_renaming_rules(file):
	""" read 'list-move-mouh.lst' & get tuples to search & replace """
	# raw    : '(sSearch, sReplacewith)    # sComment'
	# return : [(sSearch, sReplacewith, sComment)]
	if DEBUG1:
		print '[ READPAR @0661 ] ... Reading data_mouh file & parsing data'

	return [(eval(x)[0], eval(x)[1], x[x.find('#'):].replace('\n', '').replace('\r','')) for x in open(file, 'r')]

##################################################################

def clean_special(data):
	""" sort les tuples de data_mouh original pour mieux trier """
	# @data : [ ('search', 'replaceby', '# comment') ]
	# @ret  : [ ('search', 'replaceby') ]

	if DEBUG1:
		print "[ CLNDATA @0672 ] ... Sort les tuples de data_mouh original pour mieux trier"

	tmp=[]
	for d in data:
		tmp.append((d[0], d[1]))
	return tmp

##################################################################

def clean_flist_o(flist_del, flist_keep, data_mouh):
	""" Nettoie les liste de fichiers """
	# flist     : ['F:\\path\\to\\file.mp4']
	# data_mouh : [(sSearch, sReplacewith, sComment)]
	# data_mouh : [ "('Ma.Ag.Sh', 'Marvels.Agents.of.SHIELD')", # Marvel Agent of SHIELD ]
	global KILL_LIST, ELEMENTS_DEL, LIST_DEL

	if DEBUG1:
		print "[ CLNFLST @0741 ] ... TRI SELECTIF des flists (chasse aux DEL)"

	tmp_keep = []
	tmp_del = []

	for f in flist_keep:
		cleaned = NewfileMaker(f)
		newfname = cleaned.get_newfname(data_mouh)

		if newfname in KILL_LIST:
			tmp_del.append(f)

		for el in ELEMENTS_DEL:
			if el in newfname:
				tmp_del.append(f)

		if f not in tmp_del:
			tmp_keep.append(f)

	LIST_DEL = tmp_del

	return tmp_del, tmp_keep


def clean_flist(flist_del, flist_keep, data_mouh):
	""" Nettoie les liste de fichiers """
	# flist     : ['F:\\path\\to\\file.mp4']
	# data_mouh : [(sSearch, sReplacewith, sComment)]
	# data_mouh : [ "('Ma.Ag.Sh', 'Marvels.Agents.of.SHIELD')", # Marvel Agent of SHIELD ]
	global KILL_LIST, ELEMENTS_DEL, LIST_DEL

	if DEBUG1:
		print "[ CLNFLST @0741 ] ... TRI SELECTIF des flists (chasse aux DEL)"

	tmp_keep = []
	tmp_del = flist_del

	for f in flist_keep:
		cleaned = NewfileMaker(f)
		newfname = cleaned.get_newfname(data_mouh)

		if newfname in KILL_LIST:
			flist_del.append(f)

		for el in ELEMENTS_DEL:
			if el in newfname:
				flist_del.append(f)

		if f not in flist_del:
			tmp_keep.append(f)

	LIST_DEL = flist_del

	return flist_del, tmp_keep


##################################################################

def read_file(file, trigger=False):
	"""
	lit un fichier donné
	@arg   '/path/to/file', trigger_for_replace_dots
	@ret   'data_read'
	"""

	if DEBUG:
		print '[ READFIL @0715 ] ... Reading file %s' % os.path.basename(file)

	with open(file, 'r') as f:
		data = f.read()
		data = data.replace('\r\n', '\n')
		f.close()

	if trigger :
		data = data.replace(' ', '.')

	final = []
	for d in data.split('\n'):
		if d: final.append(d.split('#')[0])
		final = '#'.join('#'.join(final).split('\t')).split('#')

	return final


##################################################################

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

##################################################################

def get_big_data(data_films, data_series, data_tv, data_jan):
	""" Combine data tv series films en une seule liste """

	if DEBUG:
		print("[ GETBIGD @0778 ] ... Combining data tv, films, series into one big list")

	big_data = []
	for switch in ['series', 'films', 'jan']:
		for line in eval('data_' + switch):
			big_data.append((switch[:3], line, eval('DEST_FOLDER_' + switch), get_showdir(line)))
	for line in data_tv:
		big_data.append(('tv', line, DEST_FOLDER_tv, ''))
	return big_data

##################################################################

def process(big_data, flist_del, myfname, myversion, myfile):
	""" process big_data et flist_del """
	global LIST_DOUBLONS, LIST_MOVE, LIST_MKDIR, LIST_UNKNOWNS

	if DEBUG:
		print '[ PROCESS @0796 ] ... Processing *.lst and filelists'

	logname = "{fn}_{vn}_{dt}.log".format(fn=myfname,vn=myversion,dt=NOW)
	unkname = "{fn}_{vn}_{dt}_UNKNOWN.log".format(fn=myfname,vn=myversion,dt=NOW)
	#header = "JOURNAL DU   : {dt}\nEXECUTION DE {fn} {vn}\nLOCALISATION {fp}\n{ln}".format(fn=myfname,vn=myversion,dt=NOW,fp=myfile,ln="="*50)
	log_header = [\
		"JOURNAL DU   : %s" % NOW,
		"EXECUTION DE : %s %s" % (myfname, myversion),
		"LOCALISATION : %s" % myfile,
		"DEBUG  %s | DEBUG1 %s" % (str(DEBUG), str(DEBUG1)),   
		"DEBUG2 %s | DEBUG3 %s" % (str(DEBUG2), str(DEBUG3)), 
		"="*50 ]
	log_body = []

	mylog = ScriptMaker()

	# mkdir
	for x in LIST_MKDIR:
		try:
			msg = "[ MKDIR _______ ] ... Making dir ::: %s" % (SLASH.join(x.split(SLASH)[-2:]))
			if DEBUG3:
				msg = "[ MKDIR _______ ] ... mkdir '%s'" % (SLASH.join(x.split(SLASH)[-2:]))
			print msg
			if not DEBUG and not DEBUG3 :
				os.makedirs(x)
			log_body.append(msg)
		except Exception as ex:
			msg = "[ MKDIR _______ ] ERR Making %s >>> %s" % (SLASH.join(x.split(SLASH)[-2:]), ex)
			log_body.append(msg)
			pass

	# move
	n = 0
	for x, y, flag in LIST_MOVE:
		try:
			msg = "[ MOVE ________ ] ... Moving %s ::: %s" % (flag.upper(),SLASH.join(x.split(SLASH)[-2:]))
			if DEBUG2:
				n += 1
				diff = 'same name' if x.split(SLASH)[-1] == y.split(SLASH)[-1] else '-DIFF-'
				msg = "[ MOVE {num}_old_ ] ... '{oldfn}'\n".format(num="%03" % n, oldfn=x.split(SLASH)[-1])
				msg+= "[ MOVE {num}_new_ ] ... '{newfn}'\n".format(num="%03" % n, newfn=y.split(SLASH)[-1])
				msg+= "[ MOVE {num}_diff ] ... {isDiff}\n".format(num="%03" % n, isDiff='same name' if x.split(SLASH)[-1] == y.split(SLASH)[-1] else '-DIFF-')
				msg+= "[ MOVE {num}_dir_ ] ... {dir}\n".format(num="%03" % n, dir=y.split(SLASH)[-3:])
			print msg
			if not os.path.isfile(y):
				if not DEBUG and not DEBUG3:
					shutil.move(x, y)
				pass
			else:
				LIST_DOUBLONS.append(x)
				msg = "[ DUPL ________ ] +++ Existe déjà ::: %s" % (SLASH.join(x.split(SLASH)[-2:]))
				print msg
			log_body.append(msg)
		except Exception as ex:
			msg = "[ MOVE ________ ] ERR %s" % ex
			log_body.append(msg)
			pass

	# Delete
	for x in flist_del:
		msg = "[ DEL _________ ] ... Removing .%s ::: %s" % (x.split('.')[-1].upper(), SLASH.join(x.split(SLASH)[-2:]))
		print msg
		try:
			if not DEBUG and not DEBUG3:
				os.remove(x)
			else:
				msg = "[ DEL DEBUG     ] ... Pretending to remove %s" % x

			log_body.append(msg)

		except Exception as ex:
			msg = "[ DEL _________ ] ERR %s" % ex
			log_body.append(msg)
			pass

	# Doublons
	for x in LIST_DOUBLONS:
		msg = "[ DUPL ________ ] +++ Duplicate  ::: %s" % x
		print msg
		log_body.append(msg)

	# Unknowns
	if LIST_UNKNOWNS:
		myunk = ScriptMaker()

		unk_header = [\
			"JOURNAL DU   : %s" % NOW,
			"EXECUTION DE : %s %s" % (myfname, myversion),
			"LOCALISATION : %s" % myfile,
			"DEBUG %s | DEBUG1 %s | DEBUG2 %s | DEBUG3 %s" % (str(DEBUG), str(DEBUG1), str(DEBUG2), str(DEBUG3)),
			"-x- INCONNUS AU BATAILLON -x-",
			"="*50 ]

		unk_body = []

		for x in LIST_UNKNOWNS:
			msg = "[ UNKN ________ ] --- %s" % x
			print msg
			unk_body.append("%s" % x)
			log_body.append(msg)

		myunk.writeScript(unkname, unk_header, unk_body)
	mylog.writeScript(logname, log_header, log_body)


##################################################################

def process_fake(big_data, flist_del, myfname, myversion, myfile):
	global LIST_DOUBLONS, LIST_MOVE, LIST_MKDIR, LIST_UNKNOWNS

	if DEBUG:
		print '[ PROCESS @0891 ] ... FAKE processing *.lst and filelists'

	logname = "{fn}_{vn}_{dt}.log".format(fn=myfname,vn=myversion,dt=NOW)
	unkname = "{fn}_{vn}_{dt}_UNKNOWN.log".format(fn=myfname,vn=myversion,dt=NOW)
	#header = "JOURNAL DU   : {dt}\nEXECUTION DE {fn} {vn}\nLOCALISATION {fp}\n{ln}".format(fn=myfname,vn=myversion,dt=NOW,fp=myfile,ln="="*50)
	log_header = [\
		"JOURNAL DU   : %s" % NOW,
		"EXECUTION DE : %s %s" % (myfname, myversion),
		"LOCALISATION : %s" % myfile,
		"DEBUG %s | DEBUG1 %s | DEBUG2 %s | DEBUG3 %s" % (str(DEBUG), str(DEBUG1), str(DEBUG2), str(DEBUG3)),
		"="*50 ]
	log_body = []

	mylog = ScriptMaker()

	# mkdir
	for x in LIST_MKDIR:
		try:
			msg = "[ MKDIR _______ ] ... Making dir ::: %s" % (SLASH.join(x.split(SLASH)[-2:]))
			print msg
			if not DEBUG :
				#os.makedirs(x)
				print "[ PROCESS @1001 ] ... FAKE processing : faking makedir"
			log_body.append(msg)
		except Exception as ex:
			msg = "[ MKDIR _______ ] ERR %s" % ex
			log_body.append(msg)
			pass

	# move
	for x, y, flag in LIST_MOVE:
		try:
			msg = "[ MOVE ________ ] ... Moving %s ::: %s" % (flag.upper(),SLASH.join(x.split(SLASH)[-2:]))
			print msg
			if not os.path.isfile(y):
				if not DEBUG :
					#shutil.move(x, y)
					print "[ PROCESS @1016 ] ... FAKE processing : faking moving files"
				else:
					print "[ PROCESS @1016 ] ... FAKE processing : faking moving"
					print "[ -->FLAG @1017 ] ... %s" % flag.upper()
					print "[ -->ORIG @1018 ] ... %s" % x
					print "[ -->DEST @1019 ] ... %s" % y
				pass
			else:
				LIST_DOUBLONS.append(x)
				msg = "[ MOVE ________ ] ERR Existe déjà ::: %s" % (SLASH.join(x.split(SLASH)[-2:]))
				print msg
			log_body.append(msg)
		except Exception as ex:
			msg = "[ MOVE ________ ] ERR %s" %  ex
			log_body.append(msg)
			pass

	# Delete
	#print "[ 1353 ] xxx ", flist_del
	for x in flist_del:
		msg = "[ DEL _________ ] ... Removing .%s ::: %s" % (x.split('.')[-1].upper(), SLASH.join(x.split(SLASH)[-2:]))
		print msg
		try:
			#os.remove(x)
			print "[ PROCESS @1034 ] ... FAKE processing : faking removing files %s" % x
			log_body.append(msg)
		except Exception as ex:
			msg = "[ DEL _________ ] ERR %s" % ex
			log_body.append(msg)
			pass

	# Doublons
	for x in LIST_DOUBLONS:
		msg = "[ DUPL  ] ... Duplicate  ::: %s" % x
		print msg
		log_body.append(msg)

	# Unknowns
	if LIST_UNKNOWNS:
		myunk = ScriptMaker()

		unk_header = [\
			"JOURNAL DU   : %s" % NOW,
			"EXECUTION DE : %s %s" % (myfname, myversion),
			"LOCALISATION : %s" % myfile,
			"-x- INCONNUS AU BATAILLON -x-",
			"="*50 ]

		unk_body = []

		for x in LIST_UNKNOWNS:
			msg = "[ UNKN ________ ] --- %s" % x
			print msg
			unk_body.append("%s" % x)
			log_body.append(msg)

		myunk.writeScript(unkname, unk_header, unk_body)
	mylog.writeScript(logname, log_header, log_body)

##################################################################

def get_size_in_HR(size,precision=2):
	"""
	Get Human Readable size
	@usage   get_size_in_HR(get_size_in_bytes(file), 2)
	"""
	if DEBUG1:
		print("[ GETSZHR @0991 ] ... Getting HR format of size={sz}".format(sz=size))

	suffixes=['B','KB','MB','GB','TB']
	suffixIndex = 0
	while size > 1024:
		suffixIndex += 1 		#increment the index of the suffix
		size = size/1024.0 		#apply the division
	return "%.*f %s" % (precision,size,suffixes[suffixIndex])

##################################################################

def get_rep_freespace(path):
	"""
	Get how much free space a disk has
	@arg   path
	@ret   size in bytes, or -1 if path not found
	@note  get_size_in_HR(ret) to get Human Readable size
	$ python -m pip install wmi pypiwin32
	import wmi
	"""
	c = wmi.WMI()

	for d in c.Win32_LogicalDisk():
		   if d.Caption == path:
			fsp = d.FreeSpace
			return int(d.FreeSpace)
	return -1


def build_robocop(mydir, myfname, myversion, myfile):
	""" Robocop factory... almost """

	print("[ ROBOCOP @1030 ] ... Building robocopy script")

	# WATACHI WA ROBOTO
	robo_list = [x for x in get_filelist(mydir, patterns='*.bat', single_level=True, yield_folders=False)]

	# KILL ALL ROBOCOP
	for rpath in robo_list:
		r = os.path.basename(rpath)
		if r.startswith("robocop_") and r.endswith(".bat"):

			try:
				os.remove(r)
				if DEBUG1 :
					print "[ ROBOCOP @1096 ] --> Removed %s" % r

			except Exception as ex:
				if DEBUG1 :
					print "[ ROBOCOP @1100 ] xxx ERROR %s won't go away:" % r, ex
				pass

	# BUILD NEW ROBOCOP
	folder_list = []

		# header
	if os.path.isdir("S:\\"):
		disque = "S:"
	else:
		disque = "F:"

	try:
		addendum =  get_size_in_HR(get_rep_freespace(disque),precision=2) if os.name == 'nt' else '???'
	except NameError:
		print("[ 1271 ] ... Erreur avec WMI")
		addendum = '???'
		
	rob_header = [\
		'@ECHO OFF',
		'REM Robocop du %s' % NOW,
		'REM issu par %s %s @ %s' % (myfname, myversion, myfile),
		'REM Espace disponible sur %s\\ : %s' % (disque, addendum)]

	print '*' * 32
	print '\n'.join(rob_header)
	
	# TV & settings
	# rob_body  = [\
		# 'ROBOCOPY /XO "%s" S:\\MAGASIN-USB *.lst' % FULLSUBSET,
		# 'ROBOCOPY /XO "%s" "S:\\MAGASIN-USB\\TV-USB" *.*' % DEST_FOLDER_tv,
		# 'ROBOCOPY /XO "%s" "S:\\MAGASIN-USB\\TRAILERS-USB" *.*' % DEST_FOLDER_trailers]

	rob_body  = []	
		
	# choose ext
	myext_tmp = EXT_DOC + EXT_PIC + EXT_SUB + EXT_VID
	myext = []
	for x in myext_tmp:
		myext.append("*" + x)
	myext = ";".join(myext)

	# get flist on S: if available
	if os.path.isdir("S:\\"):
	
		slist = list(get_filelist("S:\\MAGASIN-USB\\FILMS-USB", "*",  single_level=False, yield_folders=False))
		
		# S:\MAGASIN-USB\FILMS-USB\THE CLOVERFIELD PARADOX (2018)\The.Cloverfield.Paradox.2018.1080p.NF.WEBRip.DDP5.1.x264-NTb-poster.jpg
		# print "********\n"
		# for s in slist: print s
		# print "\n***********"
		
		slist+= list(get_filelist("S:\\MAGASIN-USB\\SERIES-USB", "*", single_level=False, yield_folders=False))
		
		slist+= list(get_filelist("S:\\MAGASIN-USB\\TRAILERS-USB", "*", single_level=False, yield_folders=False))
		
		slist+= list(get_filelist("S:\\MAGASIN-USB\\TV-USB", "*", single_level=False, yield_folders=False))

		slist_tmp = []
		for x in slist:
			slist_tmp.append(x.split(SLASH)[-1])
		slist = slist_tmp
	else:
		slist = []

	# films
	flist = list(get_filelist(DEST_FOLDER_films, myext, single_level=False, yield_folders=False))
	
	# F:\MAGASIN-F1\FILMS-F2\THE CLOVERFIELD PARADOX (2018)\The.Cloverfield.Paradox.2018.1080p.NF.WEBRip.DDP5.1.x264-NTb-poster.jpg
	#print "********\n"
	#for s in flist: print s
	#print "\n***********"
	
	for f in flist:
		fname = f.split(SLASH)[-1]
		dname = f.split(SLASH)[-2]
		fpath = os.path.dirname(f)
		# F:\MAGASIN-F1\FILMS-F2\AU REVOIR LA HAUT (2017)\.actors
		# print fpath
		if fname not in slist and dname not in ANTI_POPO and dname not in ['artwork', '.actors']:
			msg = 'ROBOCOPY "%s" "%s" *.*' % (fpath, fpath.replace(DEST_FOLDER_films, "S:\\MAGASIN-USB\\FILMS-USB"))
			if msg not in rob_body:
				print msg
				rob_body.append(msg)

	# series
	flist = list(get_filelist(DEST_FOLDER_series, myext,  single_level=False, yield_folders=False))
	for f in flist:
		fname = f.split(SLASH)[-1]
		dname = f.split(SLASH)[-2]
		fpath = os.path.dirname(f)
		#options = "/MOVE /S" if dname in LISTE_POPO else ""
		#print('1081 ... fpath %s ||| ROBOCOPY %s "%s" "S:\\SERIES-USB\\%s" *.*' % (fpath, options, fpath, dname))
		if fname not in slist and dname not in ANTI_POPO and dname not in ['artwork', '.actors']:
			options = "/MOVE /S" if dname in LISTE_POPO else ""
			if DEST_FOLDER_jan in fpath: 
				dname = 'JAN\\' + dname 
			msg = 'ROBOCOPY %s "%s" "S:\\MAGASIN-USB\\SERIES-USB\\%s" *.*' % (options, fpath, dname)
			if msg not in rob_body:
				print(msg)
				rob_body.append(msg)
				
	# trailers
	tlist = list(get_filelist(DEST_FOLDER_trailers, myext, single_level=False, yield_folders=False))
	
	for f in tlist:
		fname = f.split(SLASH)[-1]
		fpath = os.path.dirname(f)
		# F:\MAGASIN-F1\FILMS-F2\AU REVOIR LA HAUT (2017)\.actors
		# print fpath
		if fname not in slist :
			msg = 'ROBOCOPY "%s" "%s" *.*' % (fpath, fpath.replace(DEST_FOLDER_trailers, "S:\\MAGASIN-USB\\TRAILERS-USB"))
			if msg not in rob_body:
				print msg
				rob_body.append(msg)
				
	# tv
	tvlist = list(get_filelist(DEST_FOLDER_tv, myext, single_level=False, yield_folders=False))
	
	for f in tvlist:
		fname = f.split(SLASH)[-1]
		fpath = os.path.dirname(f)
		# F:\MAGASIN-F1\FILMS-F2\AU REVOIR LA HAUT (2017)\.actors
		# print fpath
		if fname not in slist :
			msg = 'ROBOCOPY "%s" "%s" *.*' % (fpath, fpath.replace(DEST_FOLDER_tv, "S:\\MAGASIN-USB\\TV-USB"))
			if msg not in rob_body:
				print msg
				rob_body.append(msg)
				
	print '*' * 32

	rob_body = anti_doublons(rob_body)

	rob = ScriptMaker()
	rob.writeScript("robocop_%s.bat" % NOW, rob_header, rob_body)


def empties(dir, count=0, msg=[0]):
	""" delete empty dirs 'empties(dir)' """

	if DEBUG1 :
		print("[ DELEMP1 @1096 ] ... Deleting empty dirs'")

	for dirpath, dirnames, fnames in os.walk(dir):
		try:
			os.rmdir(dirpath)
			print "[ DELEMP1 @1096 ] ... Empty dir deleted ::: %s" % '/'.join(dirpath.split(SLASH)[-2:])
			empties(dir, count+1)
		except:
			pass
	msg.append(count)
	return '--> %i dossiers vides supprimes' % max(msg)


def detect_doublons_wide(flist):
	""" Detecter les fichiers doublons partout et pas seulement dans DEST_FOLDER """
	global LIST_DOUBLONS

	if DEBUG:
		print("[ ANTIDB2 @1112 ] ... Detecting dup files everywhere (source & dest)")

	uniques = []
	tmp = []
	final = {}
	i=0
	for f in flist:
		i+=1
		if DEBUG1 :
			print "[ ANTIDB2 @1126 ] ... flist :::", i, os.path.basename(f)
	if DEBUG1 :
			print "[ ANTIDB2 @1128 ] ... list doublons :::", LIST_DOUBLONS
	for f in flist:
		fname = os.path.basename(f)
		if DEBUG1 :
			print "[ ANTIDB2 @1131 ] ... fname  :::", fname
		if fname not in uniques:
			if DEBUG1 :
				print "[ ANTIDB2 @1134 ] ... UNIQUE ::: %s" % fname
			uniques.append(f)
		else:
			if DEBUG1 :
				print "[ ANTIDB2 @1039 ] ... DOUBLE ::: %s" % fname
			LIST_DOUBLONS.append(f)
			tmp.append(fname)
			final[fname] = tmp.count(fname)
			if DEBUG1 :
				print "[ ANTIDB2 @1144 ] ... doublon count ::: %s x%d" % (fname, tmp.count(fname))
	if DEBUG1 :
		print "[ ANTIDB2 @1146 ] ... liste doublons :::", final

	for key in final.keys():
		print "[ TEST    @1147 ] --> %s x%02i" % (key, final[key])


def display_lists():
	print "*"*25
	for x in LIST_DOUBLONS:
		print "doublons ::: %s" % x
	for x in LIST_MKDIR:
		print "mkdir    ::: %s" % x
	for x, y, flag in LIST_MOVE:
		print "move %s ::: %s --> %s" % (flag, x, y)
	for x in LIST_DEL:
		print "DEL      ::: %s" % x
	for x in LIST_UNKNOWNS:
		print "unknowns ::: %s" % x


###########################################################

def write_tvshow_nfo(xml_file, dico) :
	""" Pour produire le nfo du show uniquement """
	
	if not os.path.isfile(xml_file) and flist_temp :
		gtemp = []
		for g in dico['genres']:
			gtemp.append('    <genre>%s</genre>' % g)
	
		xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>']
		xml+= ['<tvshow>']
		xml+= ['    <title>%s</title>' % dico['title']]
		xml+= ['    <showtitle>%s</showtitle>' % dico['showtitle']]
		xml+= ['    <season>%s</season>' % dico['max_season']]
		xml+= ['    <episode>%s</episode>' % dico['max_episode']]
		xml+= ['    <plot>%s</plot>' % dico['plot']]
		xml+= ['    <outline>%s</outline>' % dico['outline']]
		xml+= ['    <tagline>%s</tagline>' % dico['tagline']]
		xml+= ['    <year>%s</year>' % dico['annee']]
		xml+= gtemp
		xml+= ['    <credits>%s</credits>' % dico['credits']]
		xml+= ['    <studio>%s</studio>' % dico['studio']]
		xml+= ['    <status>%s</status>' % dico['status']]
		xml+= ['</tvshow>']	

		if DEBUG : 
			print("[ PARWRTV @3002 ] ... Ecriture de %s" % xml_file)
			print('\n'.join(xml))
		if not DEBUG :
			with open(xml_file, 'w') as flux:
				flux.write('\n'.join(xml))
				flux.close()
				
###########################################################
		
def fix_season_episode(string):
	""" 
	Fix season & ep writing 
	
	@ver 20181011_0045
	@arg a string
	@ret a string
	"""
	if DEBUG:
		print("[ FIXSE   @2730 ] ... Fix Season & Episode writing")
		print("[ FIXSE   @2730 ] ... in : %s" % string)
		
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
		
		return "%s%s%s.%s" % (debut, saison, episode, reste)
	else:
		if DEBUG :
			print("[ FIXSE   @2730 ] ... out: %s" % string)
		return string
		
###########################################################
		
def rename_inside(fname):
	""" 
	Renommage interne de filename
	
	@ver    20181010_2030
	@arg    old fname
	@ret    new fname
	"""
	global RENAME_INSIDE
	
	if DEBUG:
		print("[ RENINS  @2720 ] ... Rename inside fname ::: %s" % fname)

	if DEBUG:
		print("[ RENINS  @2720 ] ... in : %s" % fname)

	i = 0
	while i < len(RENAME_INSIDE) :
		for i in range(len(RENAME_INSIDE)):
			if RENAME_INSIDE[i][0] in fname :
				fname = fname.replace(RENAME_INSIDE[i][0], RENAME_INSIDE[i][1])
				i = 0
			else :
				i += 1
	
	ext = os.path.splitext(fname)[1]
	regex = r'[\s._]France[\s.]4[\s._]\d{4}_[\d_]+%s' % ext
	fname = re.sub(regex, ext, fname, flags=re.IGNORECASE)
	
	if DEBUG:
		print("[ RENINS  @2720 ] ... out: %s" % fname)
			
	return fname		

	
	
##################################################################
### REWRITE OF list-move-mouh.lst ################################
##################################################################

def rewrite_lst(lst):
    """ Rewrite list of shows and films """

    # Read data from lst
    with open(lst, 'r') as f:
        data = f.read()
        f.close()

    # Clean
    hitlist = [ \
	 ('’', "."),
         (' ', '.'),
         ('..', '.'),
	 ('&amp;', '&'),
	 ('\xc2\xb0', 'o'),
	 ('\xc3\xa9', 'e'),
	 ('\xc3\xa89', 'e'),
	 ('\xc3\xa0', 'a'),
	 ('\xb4', '.'),
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
	 ('\x92', '.'),
	 ('\xe2', 'a')]
	
    data = data.replace('\r', '\n')
    data = data.replace('\n\n', '\n')

    for i in range(len(hitlist)):
        if hitlist[i][0] in data:
            data = data.replace(hitlist[i][0], hitlist[i][1])
            i = 0
   
    # Capitulize
    tmp = []
    data = data.split('\n')
    for d in data:
        if d and d.title() not in tmp:
            tmp.append(d.title())

    tmp.sort()
    data = '\n'.join(tmp)

    # Rewrite
    if not DEBUG :
        with open(lst, 'w') as g:
            g.write(data)
            g.close()
    else:
        print "[ RWCFRAM @.... ] ... Rewriting %s" % lst
        print data
        print "*" * 60


def rewrite_cfram_mouh():
	""" setup pour reecrire CFRAM_mouh """
	if DEBUG2:
		print "[ RWCFRAM @1500 ] ... Rewriting %s" % os.path.basename(CFRAM_mouh)
	cfram_inst = ScriptMaker()
	newdata = cfram_inst.readScript(CFRAM_mouh, anti_doublons=True, remove_eol=True)
	msg = prepare_for_rewrite(newdata)
	cfram_inst.writeScript(CFRAM_mouh, msg)


def prepare_for_rewrite(data):
	""" prepare data a reecrire dans CFRAM_mouh """
	if DEBUG2:
		print "[ RWCFRAM @1510 ] ... Sorting data from", os.path.basename(CFRAM_mouh)

	# build a catalog = { comment: show}
	tmp = {}
	i = 1
	for d in data:
		d = d.replace('# ', '#')
		x = d.split('#')
		if len(x) < 2:
			comment = '##%03i' % i
			tup = x[0]
			i += 1
		else:
			comment = x[1]
			tup = x[0]
		while comment.endswith(' ') or comment.endswith('\t'):
			comment = comment[:-1]
		while tup.endswith(' ') or tup.endswith('\t'):
			tup = tup[:-1]
		tmp[comment] = tup

	# find longest string chaine in the file (tuples only)
	count = []
	for key in tmp.keys():
		if not key.startswith('##'):
			count.append(len(tmp[key]))

	len_max = max(count) + 10

	# prepare msg to write
	msg = []
	for key in sorted(tmp.keys()):
		tup = tmp[key]
		if key.startswith('##'):
			comment = ''
			espace = 0
		else:
			comment = '# ' + key
			espace = len_max - len(tup)
		msg.append("%s%s%s" % (tup, " " * espace, comment))
	return msg

		

##################################################################
#### M A I N S         ###########################################
##################################################################




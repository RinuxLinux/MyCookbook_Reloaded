#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......archivage
#EXT.......py
#MAJOR....9
#MINOR....3
#DESCR....envoie fichiers des ARCHIVES vers TOTOR (ARCHIVES, pas Magasin)
#USAGE....
MYFNAME = 'archivage'
MYVERSION = 'v9.3'

"""
CHANGELOG:
	2017-09-22 v9.3     Changement option Robocopy /MOVE /S
	2017-09-19 v9.2     Réactivation de rewrite_lst(file)
	2017-09-19 v9.1     Ajout au script produit final boucle for dir robocopy dir dir /S /MOVE pour del empties 
	2017-08-28 v9.0     nouveau systeme de flag, plus detaille
	2017-08-24 v8.2     modif robocop input
	2017-07-23 V8.1     Minor fixes for 1st real test
	2017-07-21 v8.0     Changement de tactique: production d'un script robocopy.bat
	2017-07-17 v7.4     Fix probleme de point a la fin des mots dans *archives.lst
	2017-07-17 v7.3     Fix autoexec (MYVERSION dans le nom des log issus du bat)
	2017-07-16 v7.2     minor fixes
	2017-07-14 v7.1     Finalisation (1ere version utilisable)
	2017-06-30 v7.0     Reecriture encore
	2017-03-26 v6.0     Reecriture depuis le depart
	2017-03-25 v5.0     Amelioration du procede
	2017-03-16 win-v6.1 Convertion EOL Win
	2017-03-16 v6.2     Prototypage
	2017-03-16 lin-v6.1 Convertion EOL Unix
"""

import os, sys, time
import wmi
import fnmatch
import sqlite3
import hashlib
import shutil
from subprocess import call

#=============#
DEBUG = False
#DEBUG  = True
#=============#



print '***********************'
print '**** DEBUG IS %s  ****' % ('ON ' if DEBUG else 'OFF')
print '***********************'


# # # # # # #
# VARIABLES #
# # # # # # #
MYOS = os.name
if MYOS == "posix":
	USER = os.environ['USER']
	HOME = os.environ['HOME']
	if os.uname()[1] == 'debian8-TITAN':
		DEST_FOLDER = "/media/%s/Totor/FILMS_SERIES" % USER
		LOCATION_CFRAM_mouh = "/media/%s/Playground/DL/Mouh-x/moutou-settings" % USER
	else:
		DEST_FOLDER = "%s/LABO/test-archivage/Totor" % HOME
		LOCATION_CFRAM_mouh = "%s/LABO/test-archivage/Playground/DL/Mouh-x" % HOME
else:
	DEST_FOLDER = "T:\\FILMS_SERIES"
	LOCATION_CFRAM_mouh = "F:\\DL\\Mouh-x\\moutou-settings"

DEST_FOLDER_ser = os.path.join(DEST_FOLDER, 'SERIES')
DEST_FOLDER_fil = os.path.join(DEST_FOLDER, 'FILMS')
DEST_FOLDER_tv  = os.path.join(DEST_FOLDER, 'DOCUS')

DISK = "T:"

NOW = time.strftime("%Y-%m-%d_%H%M%S")
SLASH  = os.sep
NL     = os.linesep
MYPATH = os.path.dirname(os.path.abspath(__file__))
MYFILE = os.path.abspath(__file__)
AUTOEXEC = os.path.join(MYPATH, '%s_%s_autoexec.bat' % (MYFNAME, MYVERSION))

print 'EXECUTION DE %s %s %s %s' % (MYFNAME, MYVERSION, NOW, MYFILE)

# Fichiers de parametres
RULES_OF_RENAMING  = SLASH.join([LOCATION_CFRAM_mouh, "list-move-mouh.lst"])  ## ('aniurl-aot.', 'Attack.on.Titan.')				    	# Attack on Titan
RULES_OF_ARCHIVING = SLASH.join([MYPATH, "list-move-archives.lst"])           ## fil Doctor.Strange.2016

# Base de donnees SQLite
DB_NAME         = 'archivage.db'
SQL_SCRIPT_NAME = 'archivage_maj_db.sql'
DB_PATH         = SLASH.join([MYPATH, DB_NAME])
SQL_SCRIPT_PATH = SLASH.join([MYPATH, SQL_SCRIPT_NAME])
LIST_TABLES = [\
	'tbl_param_renaming',
	'tbl_param_archiving',
	'tbl_logs',
	'tbl_logs_DEBUG',
	'tbl_flag_vs_destination']

TBL_PARAM_ARCH = 'tbl_param_archiving'
TBL_PARAM_REN  = 'tbl_param_renaming'

RENAME_INSIDE = [\
		('Saison.', 'S0'),
		('.Episode.', 'E0'),
		('.MaChO@zone-telechargement.com', ''),
		('@zone-telechargement.com', ''),
		('MyVideoLinks', ''),
		('MyVideoLink', ''),
		('MyVideo', ''),
		('-DDLFR.ORG', ''),
		('[eztv]', ''),
		('\xc2\xb0', 'o'),
		('\xb0', 'o'),
		('\xe8', 'e'),
		('\xe0', 'a'),
		('\xf4', 'o'),
		('\xe7', 'c'),
		('\xe9', 'e'),
		('\xea', 'e'),
		('\xf9', 'u'),
		('+', '.'),
		(' ', '.'),
		('.-.', '_'),
		('._.', '_'),
		(',', '.'),
		('..', '.'),
		("'", '.')]


# # # # # # # # # # #
# F O N C T I O N S #
# # # # # # # # # # #

def tee_autoexec():
	""" Creer le fichier .bat qui permet d'executer le script en loggant stderr/out """
	global AUTOEXEC, MYPATH
	if not os.path.isfile(AUTOEXEC) and os.name == "nt":
		with open(AUTOEXEC, 'w') as f:
			f.write('rem cd /d "%s"\n' % MYPATH)
			f.write('{fn}_{vn}.py 1> {fn}_{vn}_stdout.log 2> {fn}_{vn}_stderr.log\n'.format(fn=MYFNAME,vn=MYVERSION))
			f.close()

			
def anti_doublons(liste, sort=False):
	'''
	tri les doublons et elimine les elements nuls
	'''
	if DEBUG: print '--- --> Anti-doublons'
	temp = []
	for element in liste:
		if element not in temp and element:
			temp.append(element)
	if sort:
		temp.sort()
	return temp


def safeguard_isDir(dirlist):
	if DEBUG: print '--- --> Safeguard isDir'
	for path in dirlist:
		if not os.path.isdir(path):
			print 'Le repertoire suivant est introuvable: %s' % path
			break
			return False
	print 'Le repertoire T:\\ est present'
	print 'Espace disponible : %s' % get_size_in_HR(get_rep_freespace("T:"),precision=2)
	return True


def safeguard_isFile(filelist):
	if DEBUG: print '--- --> Safeguard isFile'
	for file in filelist:
		if not os.path.isfile(file):
			print 'Le fichier suivant est introuvable: %s' % file
			return False
	print 'Tous les fichiers necessaires sont presents.'
	return True


def db_build_query_creation_table(db_path, list_tables):
	"""
	Creation de la base de donnees from scratch

	import sqlite3
	"""

	# tbl_param_renaming      (id_ren, sSearch, sReplacewith, sComment)
	# tbl_param_archiving     (id_arch, sFlag, sStarter, sFolderName)
	# tbl_logs                (id_log, sOldfname, sNewfname, sDestination, sSize, sStatus, sError, sEntryDate)
	# tbl_logs_DEBUG          (id_log, sOldfname, sNewfname, sDestination, sSize, sStatus, sError, sEntryDate)
	# tbl_flag_vs_destination (id_flag, sFlag, sDest)
	# 						  => int | 'anF' | ['dir lvl 1', 'dir lvl 2', 'dir lvl 3']

	global NL

	if DEBUG: print '--- --> Création de la requête'

	script_create_db = [\
	'DROP TABLE IF EXISTS tbl_param_renaming;',
	'DROP TABLE IF EXISTS tbl_param_archiving;',
	'DROP TABLE IF EXISTS tbl_flag_vs_destination;',
	'CREATE TABLE IF NOT EXISTS tbl_param_renaming (',
	'    id_ren  INTEGER PRIMARY KEY NOT NULL,',
	'    sSearch         VARCHAR     UNIQUE,',
	'    sReplacewith    VARCHAR,',
	'    sComment        VARCHAR',
	');\n',
	'CREATE TABLE IF NOT EXISTS tbl_param_archiving (',
	'    id_arch  INTEGER PRIMARY KEY NOT NULL,',
	'    sFlag            VARCHAR,',
	'    sStarter         VARCHAR     UNIQUE,',
	'    sFolderName      VARCHAR',
	');\n',
	'CREATE TABLE IF NOT EXISTS tbl_logs (',
	'    id_log INTEGER PRIMARY KEY NOT NULL,',
	'    OldFname VARCHAR,',
	'    NewFname VARCHAR,',
	'    isDifferent VARCHAR,',
	'    Destination VARCHAR,',
	'    Status VARCHAR,',
	'    Size VARCHAR,',
	'    Error VARCHAR,',
	'    Entry_Date VARCHAR',
	');\n',
	'CREATE TABLE IF NOT EXISTS tbl_logs_DEBUG (',
	'    id_log INTEGER PRIMARY KEY NOT NULL,',
	'    OldFname VARCHAR,',
	'    NewFname VARCHAR,',
	'    isDifferent VARCHAR,',
	'    Destination VARCHAR,',
	'    Status VARCHAR,',
	'    Size VARCHAR,',
	'    Error VARCHAR,',
	'    Entry_Date VARCHAR',
	');\n',
	'CREATE TABLE IF NOT EXISTS tbl_flag_vs_destination (',
	'    id_flag  INTEGER PRIMARY KEY NOT NULL,',
	'    sFlag    VARCHAR UNIQUE,',
	'    sDest    VARCHAR',
	');\n',
	'INSERT OR REPLACE INTO tbl_flag_vs_destination (id_flag, sFlag, sDest) VALUES (Null,\'anF\',"FILMS_SERIES>ANIMES>FILMS_ANIMATION");',
	'INSERT OR REPLACE INTO tbl_flag_vs_destination (id_flag, sFlag, sDest) VALUES (Null,\'anS\',"FILMS_SERIES>ANIMES>SERIES_ANIMATION");',
	'INSERT OR REPLACE INTO tbl_flag_vs_destination (id_flag, sFlag, sDest) VALUES (Null,\'doc\',"FILMS_SERIES>DOCUS");',
	'INSERT OR REPLACE INTO tbl_flag_vs_destination (id_flag, sFlag, sDest) VALUES (Null,\'fil\',"FILMS_SERIES>FILMS");',
	'INSERT OR REPLACE INTO tbl_flag_vs_destination (id_flag, sFlag, sDest) VALUES (Null,\'ser\',"FILMS_SERIES>SERIES");\n']

	return script_create_db


def db_execute_query(db_path, query):
	""" execute query in string format """
	''' import sqlite3 '''

	if DEBUG:
		print '--- --> Execution de la requête'
		print query

	conn = sqlite3.connect(db_path)
	c    = conn.cursor()
	c.executescript(query)
	conn.commit()
	c.close()
	conn.close()


def db_isTables(db_path, list_tables):
	''' check si toutes les tables sont dans la db '''
	''' import sqlite3 '''
	if DEBUG: print '--- --> Verification des tables de la base de donnees'

	# 1. get table list from db
	if DEBUG: print '--- --- --> Recuperation des tables presente dans la db'
	conn = sqlite3.connect(db_path)
	c    = conn.cursor()
	data =  c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
	lst_tables_db = [x[0] for x in data]

	# 2. compare with given list_tables
	if DEBUG: print '--- --- --> Comparaison avec la liste des tables necessaires'
	tables_in_db = True
	for t in list_tables:
		if t not in lst_tables_db:
			tables_in_db = False

	return tables_in_db


def parse_archiving_rules(file):
	""" 
	parse list-move-archives.lst 
	--> 'fil Avatar.2005' 
	"""

	if DEBUG: print '--- --> Parsing Archiving Rules ... %s' % file

	no_folder = ['doc']			# flags qui se passeront de folder special
	data0 = [x.replace('\n', '').replace('\r', '') for x in open(file, 'r')]
	data0 = anti_doublons(data0)

	tmp = []
	for d in data0:
		if d and not d.startswith("#"):
			flag = d.split(' ')[0]
			starter = d.split(' ')[1].replace(' ', '.')
			folder = get_new_dirname(starter, starter) if flag not in no_folder else 'Null'
			tmp.append((flag, starter, folder))
	return tmp

def parse_renaming_rules(file):
	# raw    : '(sSearch, sReplacewith)    # sComment'
	# return : [(sSearch, sReplacewith, sComment)]
	if DEBUG: print '--- --> Getting liste of what to rename'
	return [(eval(x)[0], eval(x)[1], x[x.find('#'):].replace('\n', '').replace('\r','')) for x in open(file, 'r')]


def get_new_dirname(filename, start, Year=False):
	'''
	filename => 'The.Goldbergs.2013.S04E06.720p.HDTV.x264-AVS.sub'
	start	 => 'The.Goldbergs.2013'
	'''
	filename    = filename.replace('.', ' ').upper()
	new_dirname = start.replace('.', ' ').upper()

	if 'Marvels.Agents.of.S.H.I.E.L.D' in start:
		return "MARVEL'S AGENTS OF S.H.I.E.L.D."  # pask kodi est un peu con sur les bords

	if filename.startswith(new_dirname):
		try:
			Year = int(new_dirname[-4:])
			Show = new_dirname[:-5]
			#print('%s (%s)') % (Show, Year)
		except:
			#raise
			pass
		return new_dirname.replace('_', ' - ') if not Year else '%s (%s)' % (Show.replace('_', ' - '), Year)
	else:
		return new_dirname.replace('_', ' - ')

def db_build_query_tbl_param (table, data):
	""" Build the query that populate tables """
	# data   : [(sFlag, sStarter, sFolderName)]
	# values : id, flag, starter, folder
	# return : liste  ['INSERT INTO table VALUES (values);']

	if DEBUG: print '--- --> Build query that will populate %s' % table

	sql_msg=[]

	for d in data:
		msg_tmp = 'INSERT OR REPLACE INTO %s VALUES (Null,"%s","%s","%s");' % (table, d[0], d[1], d[2] if len(d[2]) > 2 else 'Null')
		msg_tmp = msg_tmp.replace('"Null"', 'Null')
		sql_msg.append(msg_tmp)

	return sql_msg

def db_build_query_recup_data(db_path):
	"""
	Construit les requetes necessaires pour recuperer les
	data des tables tbl_param_archiving tbl_param_renaming
	@param   path-to-db

	"""
	global DEST_FOLDER

	if DEBUG: print '--- --> Building queries that will get data from db'

	sQuery_arch = ' '.join([\
		'SELECT',
		'    tbl_param_archiving.sflag as flag,',
		'    tbl_param_archiving.sstarter as starter,',
		'    sdest as path,',
		'    tbl_param_archiving.sfoldername as folder',
		'FROM',
		'    tbl_param_archiving',
		'NATURAL JOIN',
		'    tbl_flag_vs_destination',
		'WHERE',
		'    flag = tbl_param_archiving.sFlag',
		'ORDER BY',
		'    flag, starter ASC;'])

	sQuery_ren = ' '.join([\
		'SELECT',
		'    sSearch,',
		'    sReplacewith',
		'FROM',
		'    tbl_param_renaming',
		'ORDER BY ',
		'    sSearch ASC;'])

	return sQuery_arch, sQuery_ren

def db_get_and_parse_data_taken_from_db(data_arch, data_ren, sQuery_arch, sQuery_ren):
	""" parse data taken from db """

	global DB_PATH, DEST_FOLDER

	if DEBUG: print '--- --> Get & Parse data taken from db (arch & ren)'

	if len(data_ren) < 4 or len(data_arch) < 4:
		print('Probleme : les parametre de renommage ou d\'archivage sont vides ou corrompus.')
		sys.exit('Solution : Verifier les fichier *.lst ou la bdd.')

	# DEST_FOLDER = "T:\\FILMS_SERIES"
	# recup_data = [(u'anS', u'LastMan', u'FILMS_SERIES>ANIMES>SERIES_ANIMATION', u'LASTMAN')]
	# rules_arch	[('anF', 'Big.Hero.6.2014', '(fullpath)\\BIG HERO 6 (2014)')]
	# rules_ren     [('twd7', 'The.Walking.Dead.S07E')]

	data = db_recup_data(DB_PATH, sQuery_arch)

	rules_arch = []
	for x in data:
		flag = str(x[0])
		starter = str(x[1])
		if str(x[3]) == 'None':
			fpath = os.path.join(DEST_FOLDER, SLASH.join(str(x[2]).split('>')[1:]))
		else:
			fpath = os.path.join(DEST_FOLDER, SLASH.join(str(x[2]).split('>')[1:]), str(x[3]))
		rules_arch.append((flag, starter, fpath))
	
		#DEST_FOLDER + SLASH.join(str(x[2]).split('>')) + '' if str(x[3]) == 'None' else DEST_FOLDER + SLASH.join(str(x[2]).split('>')) + SLASH + str(x[3]))

	rules_ren = [(str(x[0]), str(x[1]) if str(x[1]) else '') for x in db_recup_data(DB_PATH, sQuery_ren)]

	return rules_arch, rules_ren

def db_recup_data(db_path, query):
	'''
	return : list (of tuples)
	'''

	if DEBUG: print '--- --- --> Executing query (return data from db)'

	conn = sqlite3.connect(db_path)
	c    = conn.cursor()
	rule = c.execute(query)
	return [x for x in rule]

def get_extensions():
	""" return lists of extensions """
	if DEBUG: print '--- --> Getting lists of extensions (all, keep, del)'
	ext_vid = ['.mkv', '.mp4', '.avi', '.ts', '.mov', '.mpeg', '.mpg']
	ext_pic = ['.png', '.jpg', '.bmp']
	ext_sub = ['.srt', '.sub', '.idx', '.ass', '.ssa']
	ext_doc = ['.txt', '.nfo']
	ext_ebo = ['.pdf', '.cbr', '.cbz']
	ext_net = ['.net', '.url', '.lnk']

	ext_DEL = ext_net + ['.bmp'] + ['.txt'] + ['sample*.mkv','sample*.avi','sample*.mp4']
	ext_DEL = '*' + ';*'.join(ext_DEL) +  ';RARBG.com.mp4'

	ext_all = anti_doublons(sorted(ext_vid + ext_pic + ext_sub + ext_doc + ext_ebo + ext_net))
	ext_all = '*' + ';*'.join(ext_all)

	ext_keep = ext_vid + ext_pic + ext_sub + ext_doc
	ext_keep = '*' + ';*'.join(ext_keep)

	ext_ebo = ['.pdf', '.cbr', '.cbz']

	return ext_all, ext_keep, ext_DEL

def get_filelist(root, patterns='*', single_level=False, yield_folders=False):
	'''
	List files and directories
	'''

	if DEBUG: print '--- --> Getting filelist'

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

def get_season_dir(fname, pattern, num_season=None):
	""" Returns name of show season directory """

	if DEBUG: print '--- --- --> Getting serie\'s season foldername ("Show - Season 01")'

	fname = fname.lower().split('.')
	for i in range(0, len(fname)) :
		if fname[i].startswith('s') and 'e' in fname[i]:
			index_s = fname[i].index('s')
			index_e = fname[i].index('e')
			num_season = fname[i][index_s+1:index_e]
			#print('%s %s %s %s') % (index_s, index_e, num_season, fname[i])
			title = ' '.join(fname[0:i])
			try:
				num_season = int(num_season)
				return '%s - Season %02i' % (pattern.replace('.', ' '), num_season)
			except:
				pass
	return '%s' % pattern.replace('.', ' ').upper()

def get_new_filename(filename, data, i=0):
	'''
	filename => 'The.Goldbergs.2013.S04E06.720p.HDTV.x264-AVS.sub'
	data     => ('we.bare.bears.s02e', 'We.Bare.Bears.S02E'), ('Z.N.3', 'Z.Nation.S03E')]
	'''

	if DEBUG: print '--- --- --> Getting new filename'

	count = 0
	while i < len(data) and count < 50:
		if filename.lower().startswith(data[i][0].lower()):
			filename = filename.replace(data[i][0], data[i][1])
			i = 0
			count += 1
		else:
			i += 1
	return filename

def get_new_title(filename, max_season=25, episode_padding=2):
	""" Puts show titles in Proper Case and fix S01E23 """

	if DEBUG: print '--- --- --> Getting new show title (Proper Case) & fixing S00E00'

	for i in range(0, max_season):
		season_search = "s%.*ie" % (episode_padding, i)  # todo: adapter pour ep-pad > 2
		if season_search in filename:
			lookup = filename.find(season_search)+len(season_search) + episode_padding
			part1 = filename[0:lookup].title()
			part2 = filename[lookup:]
			filename = '%s%s' % (part1, part2)
	return filename

def renommage_interne(filename):
	"""
	Fixes internal discrepencies
	Definition en tete de script

	"""
	global RENAME_INSIDE

	if DEBUG: print '--- --- --> Filename cleaning ("inside" strings)'

	tups = RENAME_INSIDE
	i = 0
	while i < len(tups) :
		if tups[i][0] in filename:
			filename = filename.replace(tups[i][0], tups[i][1])
			i = 0
		else:
			i += 1
	return filename

def build_catalog(filelist, data_archives, data_ren, catalog={}):
	'''
	catalog[file] = [file, fname, newpath, newfname, flag]
	data_archives = [(flag, starter, fullpath)]
	data_ren      = [(starter, replace)]
	'''
	global MYPATH, SLASH
	global DEST_FOLDER, DEST_FOLDER_fil, DEST_FOLDER_ser, DEST_FOLDER_tv

	if DEBUG:   print '--- --> Building catalog'

	for file in filelist:
		oldfname = file.split(SLASH)[-1]
		oldfpath = os.path.dirname(file)
		'''
		CATALOG[file]
		0 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv',
		1 'The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv',
		2 'T:\\FILMS_SERIES\\SERIES\\THE EXPANSE\\The Expanse - Season 02',
		3 'The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv',
		4 'ser'
		'''
		catalog[file] = [file, oldfname, MYPATH, oldfname, 'UNK']
		for d in data_archives:
			flag     = d[0]
			start    = d[1]
			newpath =  d[2]
			
			if oldfname.lower().startswith(start.lower()):
				
				if flag in ['ser', 'anS']: 
					newpath = os.path.join(DEST_FOLDER_ser, d[2], get_season_dir(oldfname, start))
				if flag == 'fil': 
					newpath = os.path.join(DEST_FOLDER_fil, d[2])
				if flag == 'doc':
					newpath = os.path.join(DEST_FOLDER_doc, d[2])
				#print '576', newpath
				catalog[file] = [\
					file,
					oldfname,
					newpath,
					get_new_filename(get_new_title(renommage_interne(oldfname)), data_ren),
					flag ]

				# log_db = { \
					# 'oldfname'   : oldfname,
					# 'destination': oldpath,
					# 'newfname'   : oldfname,
					# 'isDifferent': '-',
					# 'flag'       : flag.upper(),
					# 'size'       : '666 Kb',
					# 'status'     : "DEBUG" if DEBUG else "-",
					# 'DEBUG'      : 'True' if DEBUG else '-',
					# 'error'      : "-" }

	return catalog

def act_on_catalog(catalog):
	global DEBUG
	log_msg=[]
	log_sql = []
	log_db={}
	i = 0
	for key in catalog.keys():
		flag = catalog[key][4]
		end = False

		print('[%04i00] ' + '-'*50) % i
		print '[%04i01] FILE   : %s' % (i,key)
		print '[%04i02] FNAME  : %s' % (i, os.path.basename(key))

		ref = 2

		if flag == 'DEL':
			# log_db[file]=[oldfname, destination, newfname, isDiff, FLAG, size, status, DEBUG, error_name]
			#                 0          1           2         3       4      5    6       7      8
			ref += 1

			log_db[key] = ['%s' % key, '-', '-', '-', 'DEL', '-', 6, 'DEBUG --> ON' if DEBUG else '-', '-' ]

			print '[%04i%02i] ACTION : DELETING ...' % (i, ref)

			try:
				if not DEBUG:
					ref += 1
					os.remove(key)

					log_db[key][6] = 'REMOVED'

					log_msg.append('[ DEL       ]   %s' % key)

					print '[%04i%02i] STATUS : DELETED' % (i, ref)

				else:
					ref += 2

					log_db[key][6] = 'DEBUG --> RM OK'

					log_msg.append('[ DEL DEBUG ]   %s' % key)

					print '[%04i%02i] STATUS : DELETED (DEBUG)' % (i, ref)

			except Exception as ex:
				ref += 3

				log_db[key][6] = 'DEL ERROR'
				log_db[key][8] = '%s' % ex

				log_msg.append('[ DEL ERROR ]   %s' % key)

				output = '[%04i%02i] STATUS : ERROR (remove)' % (i, ref)
				print output

		else:
			oldfile  = key
			oldfname = os.path.basename(key)
			newdir   = catalog[key][2]
			newfname = catalog[key][3]
			newfile  = os.path.join(newdir, newfname)

			if not DEBUG:
				fsize = get_size_in_HR(get_size_in_bytes(key), precision=2)
			else:
				fsize = 'DEBUG --> SIZE'

			ref += 1
			output = '[%04i%02i] SIZE   : %s' % (i, ref, fsize)
			print output

			# log_db=[oldfname, destination, newfname, isDiff, FLAG, size, status, DEBUG, error_name]
			#           0          1           2         3       4      5    6       7      8

			log_db[key] = [key, catalog[key][2], newfname, '-' if oldfname == newfname else 'DIFF', flag.upper(), fsize,'StatusIndex6', 'DEBUG --> ON' if DEBUG else '-', '-' ]

			if flag == 'UNK':
				log_db[key][6] = 'NOT_IN_FILE'
				log_msg.append('[ UNKNOWN   ]   %s' % newfname)

				ref += 1
				output = '[%04i%02i] STATUS : NOT IN FILE' % (i,ref)
				print output

				ref += 1
				print '[%04i%02i] ACTION : IGNORING.' % (i,ref)

				end = True

			else:
				try:
					if not DEBUG:
						ref += 1
						try:
							if not os.path.isdir(newdir):
								print '[%04i%02i] ACTION : MAKING DIR ... %s' % (i, ref, newdir)
								os.makedirs(newdir)

								log_msg.append('[ MKDIR ok  ]   %s' % newdir)

								ref += 1
								output = '[%04i%02i] STATUS : MKDIR ok' % (i,ref)
								print output

						except Exception as ex:
							log_db[key][6] = 'MKD_ERR'
							log_db[key][8] = '%s' % ex

							log_msg.append('[ MKDIR ERR   ]   %s' % ex)

							ref += 1
							output = '[%04i%02i] STATUS : MKDIR ERR (other than Already Exits)' % (i,ref)
							print output

						if not os.path.isfile(newfile):

							ref += 1
							print '[%04i%02i] ACTION : MOVING ...' % (i, ref)

							shutil.move(oldfile, newfile)

							log_db[key][6] = 'MOVED'

							log_msg.append('[ MOV       ]   %s --> %s' % (oldfname, newfile))

							ref += 1
							output = '[%04i%02i] STATUS : MOVED' % (i, ref)
							print output

						else:
							log_db[key][6] = 'ALREADY_THERE'

							log_msg.append('[ MOV ERROR ]   Already exists: %s' % newfile)

							ref += 1
							output = '[%04i%02i] STATUS : FILE ALREADY EXISTS' % (i, ref)
							print output

							ref += 1
							output = '[%04i%02i] ACTION : IGNORING.' % (i, ref)
							print output

							end = True

					else:
						log_db[key][6] = 'DEBUG --> MV OK'

						log_msg.append('[ MOV DEBUG ]   %s --> %s' % (oldfname, newfile))

						ref += 1
						output = '[%04i%02i] STATUS : MOVED (DEBUG)' % (i, ref)
						print output

				except Exception as ex:
					log_db[key][6] = 'MV FAILED %s' % '(DEBUG)' if DEBUG else ''
					log_db[key][8] = '%s' % ex

					log_msg.append('[ MOV ERROR ]   %s' % ex)

					ref += 1
					output = '[%04i%02i] STATUS : MOVE FAILED -- %s' % (i, ref, '(DEBUG)' if DEBUG else ex)
					print output

		ref += 1
		print('[%04i%02i] ' + '-'*50) % (i, ref)
		i += 1

	log_msg.sort()
	return log_msg, log_db

def build_robocop(catalog):
	"""
	catalog[file] = [file, fname, newpath, newfname, flag]

	CATALOG[file]
	0 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv',
	1 'The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv',
	2 'T:\\FILMS_SERIES\\SERIES\\THE EXPANSE\\The Expanse - Season 02',
	3 'The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv',
	4 'ser'

	"""
	global DEBUG
	if DEBUG:   print '--- --> Building Robocop'

	log_msg=[]
	log_sql = []
	robocop = []

	i = 0
	for key in catalog.keys():
		flag = catalog[key][4]					# 'ser'
		end = False

		print('[%04i00] ' + '-'*50) % i
		print '[%04i01] FILE   : %s' % (i,key)
		print '[%04i02] FNAME  : %s' % (i, os.path.basename(key))

		ref = 2

		if flag == 'DEL':
			ref += 1

			if not DEBUG:
				ref += 1
				robocop.append('DEL %s' % key)
				log_msg.append('[ DEL       ]   %s' % key)
				print '[%04i%02i] STATUS : SET TO BE REMOVED' % (i, ref)

			else:
				ref += 2
				robocop.append('REM   DEL %s' % key)
				log_msg.append('[ DEL DEBUG ]   %s' % key)
				print '[%04i%02i] STATUS : DELETED (DEBUG)' % (i, ref)

		else:
			oldfpath = catalog[key][0]			# 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv'  (also key)
			oldfname = catalog[key][1]			# 'The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv'
			newdir   = catalog[key][2]			# 'T:\\FILMS_SERIES\\SERIES\\THE EXPANSE\\The Expanse - Season 02'
			newfname = catalog[key][3]			# 'The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv'
			newfpath = os.path.join(newdir, newfname)	# 'T:\\FILMS_SERIES\\SERIES\\THE EXPANSE\\The Expanse - Season 02\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv'

			if not DEBUG:
				fsize = get_size_in_HR(get_size_in_bytes(key), precision=2)
			else:
				fsize = 'DEBUG --> SIZE'

			ref += 1
			output = '[%04i%02i] SIZE   : %s' % (i, ref, fsize)
			print output

			if flag == 'UNK':
				robocop.append('REM   not in file : %s' % newfname)
				log_msg.append('[ IGNORED   ]   %s' % newfname)

				ref += 1
				output = '[%04i%02i] STATUS : NOT IN FILE' % (i,ref)
				print output

				ref += 1
				print '[%04i%02i] ACTION : IGNORING.' % (i,ref)

				end = True
			
			else:
				if not os.path.isfile(newfpath):
					ref += 1
					print '[%04i%02i] DEST   : %s' % (i,ref, newdir)
					log_msg.append('[ ROBOCOPY  ]  %s *** %s' % (newdir, newfname))
					entete = 'REM ' if DEBUG else ''
					robocop.append('%sROBOCOPY /MOVE /S "%s" "%s" "%s"' % (entete, os.path.dirname(oldfpath), newdir, newfname))
				else:
					robocop.append('REM exists already "%s"' % newfpath)
					ref += 1
					output = '[%04i%02i] STATUS : ALREADY THERE' % (i,ref)
					print output
					log_msg.append('[ -EXISTS-  ]  %s *** %s' % (newdir, newfname))
		ref += 1
		print('[%04i%02i] ' + '-'*50) % (i, ref)
		i += 1

	robocop = anti_doublons(robocop, sort=True)
	log_msg.sort()
	return robocop, log_msg

def get_size_in_bytes(file):
	"""
	get file size in bytes
	import os
	"""
	st = os.stat(file)
	return st.st_size

def get_size_in_HR(size,precision=2):
	'''
	Get Human Readable size
	@usage   get_size_in_HR(get_size_in_bytes(file), 2)
	'''
	suffixes=['B','KB','MB','GB','TB']
	suffixIndex = 0
	while size > 1024:
		suffixIndex += 1 		#increment the index of the suffix
		size = size/1024.0 		#apply the division
	return "%.*f %s" % (precision,size,suffixes[suffixIndex])

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

def rewrite_lst(file):
	""" order and rewrite lst """
	# GET DATA
	data = [ x.replace('\n', '').replace('\r', '') for x in open(file, 'r') ]
	header = []
	body = []

	# ANTI-DOUBLONS 1
	for d in data:
		if d.startswith("# ") and d not in header:
			header.append(d)
		else:
			body.append(d)

	# NETTOYAGE DATA (body)
	for i in range(0, len(body)):
		while body[i].endswith('.') or body[i].endswith(' '):
			body[i] = body[i][:-1]

	# ANTI-DOUBLONS 2
	header = anti_doublons(header, sort=True)
	body = anti_doublons(body, sort=True)

	# REORGANISATION
	tmp = []
	for t in body:
		if t and t not in tmp:
			da = t.split(' ')
			tmp.append('%s %s' % (da[0], '.'.join(da[1:])))

	# REECRITURE
	with open(file, 'w') as f:
		f.write('\n'.join(header))
		f.write('\n')
		f.write('\n'.join(tmp))
		f.write('\n')
		f.close()

def db_build_query_logging(log):
	global NOW, DEBUG
	# log_db[file]=[oldfname, destination, newfname, isDiff, FLAG, size, status, DEBUG, error_name]
	#                 0          1           2         3       4      5    6       7      8

	# 'oldfname'   : oldfname,
	# 'destination': oldpath,
	# 'newfname'   : oldfname,
	# 'isDifferent': '-',
	# 'flag'       : flag.upper(),
	# 'size'       : '666 Kb',
	# 'status'     : "DEBUG" if DEBUG else "-",
	# 'DEBUG'      : 'True' if DEBUG else '-',
	# 'error'      : "-" }

	table = 'tbl_logs_debug' if DEBUG else 'tbl_logs'

	qry = [ 'DROP TABLE IF EXISTS %s;' % table,
			'CREATE TABLE IF NOT EXISTS "%s"(' % table,
			   '    [id_log] INTEGER PRIMARY KEY NOT NULL,',
			   '    [OldFname] VARCHAR,',
			   '    [Destination] VARCHAR,',
			   '    [NewFname] VARCHAR,',
			   '    [isDifferent] VARCHAR,',
			   '    [flag] VARCHAR,',
			   '    [Size] VARCHAR,',
			   '    [Status] VARCHAR,',
			   '    [debug] VARCHAR,',
			   '    [Error] VARCHAR,',
			   '    [Entry_Date] VARCHAR);']

	for val in log.values():
		val[0] = os.path.basename(val[0])
		qry.append('INSERT OR IGNORE INTO %s VALUES(Null, "%s", "%s");' % (table, '","'.join(val), NOW))

	return qry

def empties(dir, count=0, msg=[0]):
	for dirpath, dirnames, fnames in os.walk(dir):
		try:
			os.rmdir(dirpath)
			empties(dir, count+1)
		except:
			pass
	msg.append(count)
	return '--> %i dossiers vides supprimes' % max(msg)

#===============================================

def safety():
	global DEST_FOLDER, LOCATION_CFRAM_mouh
	global RULES_OF_ARCHIVING, RULES_OF_RENAMING

	isDirs  = safeguard_isDir([DEST_FOLDER, LOCATION_CFRAM_mouh])
	isFiles = safeguard_isFile([RULES_OF_ARCHIVING, RULES_OF_RENAMING])

	if not isDirs or not isFiles :
		msg = raw_input('Press Enter to exit.\n')
		sys.exit(msg)

def preparation_bdd():
	global DB_PATH, LIST_TABLES
	qry = ['PRAGMA foreign_keys=OFF;', 'BEGIN TRANSACTION;']

	## --------------------------
	## TRAITEMENT BASE DE DONNEES
	## --------------------------

	# Check si db existe ou que toutes les tables sont là
	if not os.path.isfile(db_path) or not db_isTables(db_path, LIST_TABLES):
		print 'La base de données suivante est introuvable ou incomplete: %s' % db_path
		if DEBUG:   print '--> Création de la base de données...'
	#qry.append(db_build_query_creation_table(db_path, LIST_TABLES))
	qry += db_build_query_creation_table(db_path, LIST_TABLES)

	## ----------------------------
	## UPDATE DB WITH *.LST (PARAM)
	## ----------------------------

	print 'PEUPLEMENT DE LA BASE DE DONNEES AVEC LE CONTENU DES .LST'

	# 1) Read *.lst (get new data)
	if DEBUG: print '--> Recuperation des parametres depuis les fichiers lst'
	data_arch = anti_doublons(parse_archiving_rules(RULES_OF_ARCHIVING), sort=True)  # [(sFlag, sStarter, sFolderName)]
	data_ren  = anti_doublons(parse_renaming_rules(RULES_OF_RENAMING),   sort=True)  # [(sSearch, sReplacewith, sComment)]

	# 2) prepare query pour maj tbl param arch & renom
	if DEBUG: print '--> Preparation du script d\'update'
	sql_script_path = MYPATH + SLASH + NOW + '_update_lst_to_db.sql'

	#if not DEBUG :
	qry += db_build_query_tbl_param (TBL_PARAM_ARCH, data_arch)
	qry += [' ']
	qry += db_build_query_tbl_param (TBL_PARAM_REN, data_ren)
	qry += ['COMMIT;']

	# 3) Ecrire la requete dans un fichier sql pour futur reference
	if DEBUG: print '--> Ecriture de la requete dans le fichier %s' % sql_script_path
	try:
		open(sql_script_path, 'w').write('\n'.join(qry))
	except Exception as ex:
		sys.exit('Erreur build_sql_script(script_path, lst_msg) : %s' % ex)

	# 4) Execution de la requete
	if DEBUG: print '--> Execution de la requete'
	db_execute_query(db_path, ' '.join(qry))

def update_lst():
	## ----------------------------
	## UPDATE *.LST (PARAM) WITH DB
	## ----------------------------

	print 'PEUPLEMENT DES .LST AVEC LE CONTENU DE LA BASE DE DONNEES'

	# 4) read from db
	#  - execute query1 (join)     (flag, starter, fullpath) <-- data_arch
	#  - execute query2 (select)   (starter, replace)        <-- data_ren
	sQuery_arch, sQuery_ren = db_build_query_recup_data(db_path)
	data_arch, data_ren     = db_get_and_parse_data_taken_from_db(data_arch, data_ren, sQuery_arch, sQuery_ren)

def get_file_lists():
	"""
	get list of files to delete and files to keep
	@arg   None
	@ret   list of files fullpaths x2 (keep and del)
	"""

	# 5) get extensions
	ext_all, ext_keep, ext_del = get_extensions()

	# 6) DEL
	#  - del ext      (ext_del)
	#  - del sample   (el_del)

	if not DEBUG :
		flist_del  = [ x for x in get_filelist(MYPATH, ext_del,  single_level=False, yield_folders=False)]
		flist_keep = [ x for x in get_filelist(MYPATH, ext_keep, single_level=False, yield_folders=False)]
	else:
		flist_del  = ['F:\\MAGASIN-F1\\ARCHIVES-F2\\Command Prompt.lnk']
		flist_keep = ['F:\\MAGASIN-F1\\ARCHIVES-F2\\Legion.S01E08.1080p.WEB-DL.DD5.1.H264-RARBG.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG-thumb.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG[eztv].MyVideoLink.....nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E10.1080p.WEB-DL.DD5.1.H264-RARBG-SDH.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E10.1080p.WEB-DL.DD5.1.H264-RARBG.en.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E10.1080p.WEB-DL.DD5.1.H264-RARBG.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E10.1080p.WEB-DL.DD5.1.H264-RARBG.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\LIFE IN PIECES\\Life.in.Pieces.S02E17.720p.HDTV.x264-AVS.en.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\LIFE IN PIECES\\Life.in.Pieces.S02E17.720p.HDTV.x264-AVS.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\PACIFIC RIM (2013)\\Pacific.Rim.2013.iNTERNAL.1080p.BluRay.x264-MOOVEE.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE LAST MAN ON EARTH\\The.Last.Man.On.Earth.S03E13.720p.HDTV.x264-AVS.MyVideoLinks.en.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE LAST MAN ON EARTH\\The.Last.Man.On.Earth.S03E13.720p.HDTV.x264-AVS.MyVideoLinks.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY.en.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG.srt']

	return flist_del, flist_keep

def make_catalog():
	####################
	##  BUILD CATALOG ##
	####################
	# catalog[file] = [file, fname, 'newpath', 'newname', flag, start]
	#                    0     1        2          3        4     5
	# data_arch = [(flag, starter, fullpath)]
	# 7) Build catalog
	catalog = build_catalog(flist_keep, data_arch, data_ren)

	for file in flist_del:
		catalog[file] = [file, file.split(SLASH)[-1], False, False, 'DEL']
	return catalog

	
def parse_data_arch(data):
	"""
	parse le contenu de list-move-archives.lst
	@arg   raw data [liste de lignes]
	@ret   dico { flag: (destination, [starters]) }
	"""
	# # af4 "T:\FILMS_SERIES\ANIMES\FILMS_ANIMATION\=DISNEY=\DISNEY EN VO"
	# # f13 "T:\FILMS_SERIES\FILMS\Sci-Fi\=MARVEL="
	# # ser "T:\FILMS_SERIES\SERIES"
	# anS LastMan
	# fil Captain.America.The.Winter.Soldier.2014
	# ser The.Expanse
	global MYOS, DEST_FOLDER
	temp = []
	no_folder = ['doc']	
	# Get list of flags & destinations (general listing)
	# dico1 = { flag: dest_path }
	dico_of_flags_and_destinations = {}
	for d in data:
		if d.startswith("#"):
			flag = d.split(" ")[1]
			dest = " ".join(d.split(" ")[2:]).replace('"', '')
			if MYOS == "posix": 
				dest = '/'.join([DEST_FOLDER] + dest.split("\\")[2:])
			dico_of_flags_and_destinations[flag] = dest
	
	# Get flag, destination of the names in the list
	for d in data:
	 	if not d.startswith("#"):
	 		if d.split(' ')[0] in (dico_of_flags_and_destinations.keys()):
	 			flag = d.split(' ')[0]
			 	starter = ".".join(d.split(" ")[1:]).replace(' ', '.')
				newdirname = get_new_dirname(starter, starter) if flag not in no_folder else 'Null'
	 			destination = dico_of_flags_and_destinations[d.split(' ')[0]] + SLASH + newdirname
	 			temp.append((flag, starter, destination))
	#print '1135', temp
	return temp


def main():
	tee_autoexec()
	safety()
	
	#RULES_OF_ARCHIVING = SLASH.join([MYPATH, "list-move-archives.lst"])           ## fil Doctor.Strange.2016
	archlist = "list-move-archives.lst"

	# get raw data from archlist
	data_what_to_arch = [x.replace('\r', '').replace('\n', '') for x in open(archlist, 'r')]
	
	# sort raw data into a list of tuples: t = [(flag, starter, dest)]  [('ser', 'The.Expanse', 'path/to/THE EXPANSE')]
	triple_flag_starter_dest = parse_data_arch(data_what_to_arch) 

	# skipping db update and mining for now

	# GET EXTENSIONS
	ext_all, ext_keep, ext_del = get_extensions()

	# get filelist
	if not DEBUG :
		flist_del  = [ x for x in get_filelist(MYPATH, ext_del,  single_level=False, yield_folders=False)]
		flist_keep = [ x for x in get_filelist(MYPATH, ext_keep, single_level=False, yield_folders=False)]
	else:
		flist_del  = ['F:\\MAGASIN-F1\\ARCHIVES-F2\\Command Prompt.lnk']
		flist_keep = ['F:\\MAGASIN-F1\\ARCHIVES-F2\\Legion.S01E08.1080p.WEB-DL.DD5.1.H264-RARBG.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG-thumb.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG[eztv].MyVideoLink.....nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E10.1080p.WEB-DL.DD5.1.H264-RARBG-SDH.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E10.1080p.WEB-DL.DD5.1.H264-RARBG.en.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E10.1080p.WEB-DL.DD5.1.H264-RARBG.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E10.1080p.WEB-DL.DD5.1.H264-RARBG.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\LIFE IN PIECES\\Life.in.Pieces.S02E17.720p.HDTV.x264-AVS.en.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\LIFE IN PIECES\\Life.in.Pieces.S02E17.720p.HDTV.x264-AVS.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\PACIFIC RIM (2013)\\Pacific.Rim.2013.iNTERNAL.1080p.BluRay.x264-MOOVEE.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE LAST MAN ON EARTH\\The.Last.Man.On.Earth.S03E13.720p.HDTV.x264-AVS.MyVideoLinks.en.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE LAST MAN ON EARTH\\The.Last.Man.On.Earth.S03E13.720p.HDTV.x264-AVS.MyVideoLinks.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY.en.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG.srt']

	## --------------
	##  BUILD CATALOG
	## --------------
	## catalog[file] = [file, fname, 'newpath', 'newname', flag]
	##                   0      1        2          3        4
	## data_arch     = [(flag, starter, fullpath)]

	# 7) BUILD CATALOG, BASED ON FLIST
	data_arch = triple_flag_starter_dest
	data_ren  = anti_doublons(parse_renaming_rules(RULES_OF_RENAMING),   sort=True)  # [(sSearch, sReplacewith, sComment)]
	
	catalog = build_catalog(flist_keep, data_arch, data_ren)

	for file in flist_del:
		catalog[file] = [file, False, False, False, 'DEL']


	## ---------
	##  ROBOCOP
	## ---------

	#log_msg, log_db = act_on_catalog(catalog)

	ROBOCOPY, log = build_robocop(catalog)

  	if os.name != "posix" : 
		freespace = get_size_in_HR(get_rep_freespace(DISK),precision=1)
	else:
		freespace = "<linux says nay!>"

	del_empties = 'for /f "usebackq delims=" %d in (`"dir /ad/b/s | sort /R"`) do robocopy /s /move "%d" "%d"'

	with open('robocop_%s_%s.bat.log' % (MYVERSION,NOW), 'w') as f:
		f.write('REM {fn}_{vn} - {dt}\n'.format(fn=MYFNAME,vn=MYVERSION,dt=NOW))
		f.write('REM %s espace disponible sur %s\\\n' % (freespace, DISK))
		f.write('REM cd /d "%s"\n' % MYPATH)
		f.write('\n'.join(ROBOCOPY) + NL)
		f.write(del_empties)
		f.close()

	## -------------
	##  LOG JOURNALS
	## -------------
	
	# LOG ACTIONS INTO *.LOG FILE
	logname = '%s_%s_%s.log' % (MYFNAME, MYVERSION, NOW)
	logfile = os.path.join(MYPATH, logname)
	with open(logfile, 'w') as f:
		head1 = 'JOURNAL de {fn} {vn}, le {dt}\n'.format(fn=MYFNAME,vn=MYVERSION,dt=NOW)
		head2 = '%s\n' % MYFILE
		f.write(head1)
		f.write(head2)
		f.write('='*len(head2)+'\n')
		f.write('DEBUG IS %s\n' % ('ON ' if DEBUG else 'OFF'))
		f.write('************\n')
		f.write('\n'.join(log))
		f.close()

	if not DEBUG:
		rewrite_lst(RULES_OF_ARCHIVING)
	else:
		print "[ NOTE  ] DEBUG is %s, therefore re-writing of *.lst is skipped!" % DEBUG
	



def main2():
	global MYPATH, NL, SLASH, NOW, DEBUG, DISK
	global DEST_FOLDER, LOCATION_CFRAM_mouh
	global RULES_OF_ARCHIVING, RULES_OF_RENAMING
	global SQL_SCRIPT_NAME, SQL_SCRIPT_PATH
	global DB_NAME, DB_PATH, LIST_TABLES
	global TBL_PARAM_ARCH, TBL_PARAM_REN
	global MYFNAME, MYVERSION, MYFILE

	tee_autoexec()

	qry = ['PRAGMA foreign_keys=OFF;', 'BEGIN TRANSACTION;']

	## ------------
	## SAFEGUARDS : verifie existence des repertoires/fichiers necessaires au bon fonctionnement
	## ------------

	isDirs  = safeguard_isDir([DEST_FOLDER, LOCATION_CFRAM_mouh])
	isFiles = safeguard_isFile([RULES_OF_ARCHIVING, RULES_OF_RENAMING])

	if not isDirs or not isFiles :
		msg = raw_input('Press Enter to exit.\n')
		sys.exit(msg)

	## --------------------------
	## TRAITEMENT BASE DE DONNEES
	## --------------------------

	# Check si db existe ou que toutes les tables sont là
	if not os.path.isfile(DB_PATH) or not db_isTables(DB_PATH, LIST_TABLES):
		print 'La base de données suivante est introuvable ou incomplete: %s' % DB_PATH
		if DEBUG: print '--> Création de la base de données...'
	#qry.append(db_build_query_creation_table(DB_PATH, LIST_TABLES))
	qry += db_build_query_creation_table(DB_PATH, LIST_TABLES)

	## ----------------------------
	## UPDATE DB WITH *.LST (PARAM)
	## ----------------------------

	print 'PEUPLEMENT DE LA BASE DE DONNEES AVEC LE CONTENU DES .LST'

	# 1) READ *.LST (GET NEW DATA)
	if DEBUG: print '--> Recuperation des parametres depuis les fichiers lst'
	data_arch = anti_doublons(parse_archiving_rules(RULES_OF_ARCHIVING), sort=True)  # [(sFlag, sStarter, sFolderName)]
	data_ren  = anti_doublons(parse_renaming_rules(RULES_OF_RENAMING),   sort=True)  # [(sSearch, sReplacewith, sComment)]

	# 2) PREPARE QUERY POUR MAJ TBL PARAM ARCH & RENOM
	if DEBUG: print '--> Preparation du script d\'update'
	sql_script_path = MYPATH + SLASH + NOW + '_update_lst_to_db.sql'

	#if not DEBUG :
	qry += db_build_query_tbl_param (TBL_PARAM_ARCH, data_arch)
	qry += [' ']
	qry += db_build_query_tbl_param (TBL_PARAM_REN, data_ren)
	qry += ['COMMIT;']

	# 3) ECRIRE LA REQUETE DANS UN FICHIER SQL POUR FUTUR REFERENCE
	if DEBUG: print '--> Ecriture de la requete dans le fichier %s' % sql_script_path
	try:
		open(sql_script_path, 'w').write('\n'.join(qry))
	except Exception as ex:
		sys.exit('Erreur build_sql_script(script_path, lst_msg) : %s' % ex)

	# 4) EXECUTION DE LA REQUETE
	if DEBUG: print '--> Execution de la requete'
	db_execute_query(DB_PATH, ' '.join(qry))


	## ----------------------------
	## UPDATE *.LST (PARAM) WITH DB
	## ----------------------------

	print 'PEUPLEMENT DES .LST AVEC LE CONTENU DE LA BASE DE DONNEES'

	# 4) READ DATA FROM DB
	#  - execute query1 (join)     (flag, starter, fullpath) <-- data_arch
	#  - execute query2 (select)   (starter, replace)        <-- data_ren
	sQuery_arch, sQuery_ren = db_build_query_recup_data(DB_PATH)
	data_arch, data_ren     = db_get_and_parse_data_taken_from_db(data_arch, data_ren, sQuery_arch, sQuery_ren)

	## ----------------------
	## GET & ANALYZE FILELIST
	## ----------------------

	print 'ANALYSE DES FICHIERS'

	# 5) GET EXTENSIONS
	ext_all, ext_keep, ext_del = get_extensions()

	# 6) DEL
	#  - del ext      (ext_del)
	#  - del sample   (el_del)

	if not DEBUG :
		flist_del  = [ x for x in get_filelist(MYPATH, ext_del,  single_level=False, yield_folders=False)]
		flist_keep = [ x for x in get_filelist(MYPATH, ext_keep, single_level=False, yield_folders=False)]
	else:
		flist_del  = ['F:\\MAGASIN-F1\\ARCHIVES-F2\\Command Prompt.lnk']
		flist_keep = ['F:\\MAGASIN-F1\\ARCHIVES-F2\\Legion.S01E08.1080p.WEB-DL.DD5.1.H264-RARBG.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG-thumb.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E09.1080p.WEB-DL.DD5.1.H264-RARBG[eztv].MyVideoLink.....nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E10.1080p.WEB-DL.DD5.1.H264-RARBG-SDH.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E10.1080p.WEB-DL.DD5.1.H264-RARBG.en.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E10.1080p.WEB-DL.DD5.1.H264-RARBG.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\The.Expanse.S02E10.1080p.WEB-DL.DD5.1.H264-RARBG.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\LIFE IN PIECES\\Life.in.Pieces.S02E17.720p.HDTV.x264-AVS.en.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\LIFE IN PIECES\\Life.in.Pieces.S02E17.720p.HDTV.x264-AVS.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\PACIFIC RIM (2013)\\Pacific.Rim.2013.iNTERNAL.1080p.BluRay.x264-MOOVEE.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE LAST MAN ON EARTH\\The.Last.Man.On.Earth.S03E13.720p.HDTV.x264-AVS.MyVideoLinks.en.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE LAST MAN ON EARTH\\The.Last.Man.On.Earth.S03E13.720p.HDTV.x264-AVS.MyVideoLinks.mkv', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY.en.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\THE WOLVERINE (2013)\\The.Wolverine.2013.1080p.BluRay.x264.YIFY.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN (2000)\\X-Men.2000.1080p.BrRip.x264.YIFY.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN ORIGINS WOLVERINE (2009)\\X-Men.Origins.Wolverine.2009.1080p.BrRip.x264.YIFY.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X-MEN THE LAST STAND (2006)\\X-Men.The.Last.Stand.2006.1080p.BrRip.x264.YIFY.srt', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG-fanart.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG-poster.jpg', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG.mp4', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG.nfo', 'F:\\MAGASIN-F1\\ARCHIVES-F2\\X2 X-MEN UNITED (2003)\\X2.X-Men.United.2003.1080p.BluRay.H264.AAC-RARBG.srt']


	## --------------
	##  BUILD CATALOG
	## --------------
	## catalog[file] = [file, fname, 'newpath', 'newname', flag]
	##                   0      1        2          3        4
	## data_arch     = [(flag, starter, fullpath)]

	# 7) BUILD CATALOG, BASED ON FLIST

	catalog = build_catalog(flist_keep, data_arch, data_ren)

	for file in flist_del:
		catalog[file] = [file, False, False, False, 'DEL']


	## ---------------
	##  ACT ON CATALOG
	## ---------------

	#log_msg, log_db = act_on_catalog(catalog)

	ROBOCOPY, log = build_robocop(catalog)

  	if os.name != "posix" : 
		freespace = get_size_in_HR(get_rep_freespace(DISK),precision=1)
	else:
		freespace = "<linux says nay!>"

	with open('robocop_%s_%s.bat.log' % (MYVERSION,NOW), 'w') as f:
		f.write('REM {fn}_{vn} - {dt}\n'.format(fn=MYFNAME,vn=MYVERSION,dt=NOW))
		f.write('REM %s espace disponible sur %s\\\n' % (freespace, DISK))
		f.write('REM cd /d "%s"\n' % MYPATH)
		f.write('\n'.join(ROBOCOPY))
		f.close()

	## -------------
	##  LOG JOURNALS
	## -------------
	
	# LOG ACTIONS INTO *.LOG FILE
	logname = '%s_%s_%s.log' % (MYFNAME, MYVERSION, NOW)
	logfile = os.path.join(MYPATH, logname)
	with open(logfile, 'w') as f:
		head1 = 'JOURNAL de {fn} {vn}, le {dt}\n'.format(fn=MYFNAME,vn=MYVERSION,dt=NOW)
		head2 = '%s\n' % MYFILE
		f.write(head1)
		f.write(head2)
		f.write('='*len(head2)+'\n')
		f.write('DEBUG IS %s\n' % ('ON ' if DEBUG else 'OFF'))
		f.write('************\n')
		f.write('\n'.join(log))
		f.close()

	"""
	# LOG ACTIONS INTO *.DB
	qry = db_build_query_logging(log_db)
	with open(SQL_SCRIPT_PATH, 'w') as f:
		f.write('\n'.join(qry))
		f.close()
	db_execute_query(DB_PATH, '\n'.join(qry))
	"""
	
	# REWRITE ARCHIVES.LST
	rewrite_lst(RULES_OF_ARCHIVING)

	# CHECK DISK SPACE ON DEST_FOLDER

	# RED
	print empties(MYPATH)


# # # # # #
# B O D Y #
# # # # # #

#NOW = get_time()   # obsolete
main()
#for key, tup1, tup2 in {'cle0': ("val1", [1])}: print tup2
#!/usr/bin/env python
#-*- coding: utf-8 -*-
# 2017-12-21
# get ebooks md5 & compare to db, export newfname into csv

##################################################################
#### S E T U P         ###########################################
##################################################################

import os, time, fnmatch, sys
import hashlib, sqlite3

# CHANGELOG
# 2019-01-05 v5.2   Version pour faire un dir avec VERBATIM
# 2018-12-04 v5.1   test new sh script (if then doublons)
# 2018-11-30 v5.0   new sqlite db schema
# 2017-03-16 v4.0   grand nettoyage + renommage du script ?
# 2017-03-15 v3.2   ajout rmdir dans script move.sh
# 2017-03-14 v3.1   adaptation any path (mypath)
# 2017-12-21 v3.0   refonte
# 2017-10-09 v2.16  ajout BD
# 2017-10-05 v2.15  ajout colonne dans csv
# 2017-10-01 v2.13  chacun sa db ici c'est la v3
# 2017-10-01 v2.1   minor fixes
# 2017-09-30 v2.0   implementation myebooks_v3.db
# 2017-09-28 v1.5   modif masque renommage

MYFNAME   	= "chkdb5"
MYVERSION 	= "v5.2"
MYEXT		= ".py"
MYDESCR		= " get ebooks md5 & compare to db, export newfname into csv"
MYUSAGE		= "$ python {fn}".format(fn=os.path.basename(os.path.abspath(__file__)))

NOW = time.strftime("%Y-%m-%d_%H%M%S")
SLASH  = os.sep
NL     = os.linesep
MYPATH = os.path.dirname(os.path.abspath(__file__))
MYFILE = os.path.abspath(__file__)
AUTOEXEC = os.path.join(MYPATH, '%s_%s_autoexec.bat' % (MYFNAME, MYVERSION))

#=============#
DEBUG  = False
DEBUG1 = False   # debug + detaillé
DEBUG2 = False   # utilisation de la vraie flist
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
	if sys.argv[1].upper() == 'VERSION':
		sys.exit("--> %s %s" % (MYFNAME, MYVERSION))
	if sys.argv[1].upper() == 'USAGE':
		msg = ["USAGE"]
		msg+= ["     $ python {mf}".format(mf=os.path.basename(MYFILE))]
		msg+= ["OPTIONS"]
		msg+= ["     'debug'     debuggage simple"]
		msg+= ["     'debug1'    debuggage détaillé"]
		msg+= ["     'debug2'    utilisation de la vraie flist"]
		msg+= ["     'usage'     affiche ce message"]
		msg+= ["     'version'   affiche fname et version"]
		sys.exit("\n".join(msg))


print '***********************'
print '**** DEBUG IS %s  ****' % ('ON ' if DEBUG else 'OFF')
print '***********************'
msg = 'EXECUTION DE %s %s %s\nLOCALISATION %s' % (MYFNAME, MYVERSION, NOW, MYFILE)
print msg
print '.' * (len(msg) / 2 )


##################################################################
#### G L O B A L E S   ###########################################
##################################################################

EXT_DOC = ['.txt', '.nfo']
EXT_EBO = ['.pdf', '.cbr', '.cbz', '.epub', '.azw3']
EXT_EXTRA = ['sample*.mkv','sample*.avi','sample*.mp4']
EXT_NET = ['.net', '.url', '.lnk']
EXT_PIC = ['.png', '.jpg', '.bmp']
EXT_SUB = ['.srt', '.sub', '.idx', '.ass', '.ssa']
EXT_VID = ['.mkv', '.mp4', '.avi', '.ts', '.mov', '.mpeg', '.mpg']
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

RENAME_INSIDE = [('Saison.', 'S0'),
		 		 ('Episode.', 'E0'),
				 ('S02.E', 'S02E'),
				 ('S2 - 0', 'S02E0'),
				 ('S2 - 1', 'S02E1'),
				 ('wWw.Extreme-Down.Net', ''),
		 		 ('+', '.'),
				 ('?', ''),
				 ('&amp;', '&'),
				 ('\xc2\xb0', 'o'),
				 ('\xc3\xa9', 'e'),
				 ('’', '.'),
				 ('\x83', 'a'),
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
				 ('.-.', '_'),
		 		 ('._.', '_'),
				 (',', '.'),
		 		 ('..', '.'),
		 		 ("'", '.')]

ELEMENTS_REN  = [	'[eztv]', '-DDLFR.ORG',
					'-zaphyra-telechargementz', 'www.telechargementz-streaming.com',
					'MyVideoLinks',  'MyVideoLink', 'MyVideo',
					'.MaChO@zone-telechargement.com', '@zone-telechargement.com',
					'_fr.downmagaz.com', '_downmagaz.com', '_do.az.com', '_fr.downmagaz.com',
					'wWw.Extreme-Down.Net']



# Base de donnees SQLite
DB_NAME = 'myebooks_v5.db'
TBL_NAME = 'master_v4'     # table ou trouver les donnees
#DB_PATH = SLASH.join([MYPATH, DB_NAME])
if os.name == 'nt' : 
	DB_PATH = 'Z:\\Dropbox\\LABO-DBX\\myebooks\\myebooks_v4.db'
else:
	DB_PATH = '/home/reno/Dropbox/LABO-DBX/myebooks/myebooks_v4.db'

if not os.path.isfile(DB_PATH):
	sys.exit("DB_PATH introuvable : ", DB_PATH)

#DB_PATH = 'F:\\EBOOKS-F1\\trier\\myebooks_v3.db'


##################################################################
#### C L A S S E S     ###########################################
##################################################################

class bcolors:
	""" Usage : 
	print bcolors.WARNING + "Attention !" + bcolors.ENDC
	"""
	HEADER = '\033[95m'       # Light Magenta
	OKBLUE = '\033[94m'       # Light Blue
	OKGREEN = '\033[92m'      # Light Green
	WARNING = '\033[1;97;41m' # Red BG, Bold, White FG
	FAIL = '\033[93m'         # Light Yellow
	ENDC = '\033[0m'          # End
	BOLD = '\033[1m'          # Bold
	UNDERLINE = '\033[4m'     # Underline

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

def get_extension(keep, delete):
	if DEBUG: print '--- --> Getting lists of extensions (keep, del)'
	ext_keep = '*' + ';*'.join(keep)
	ext_DEL = '*' + ';*'.join(delete) +  ';RARBG.com.mp4'
	return ext_keep, ext_DEL

def tee_autoexec():
	""" Creer le fichier .bat qui permet d'executer le script en loggant stderr/out """
	global AUTOEXEC, MYPATH, MYFNAME, MYVERSION, NOW
	if not os.path.isfile(AUTOEXEC) and os.name == "nt":
		with open(AUTOEXEC, 'w') as f:
			f.write('REM EXECUTION DE %s\n' % MYFILE)
			f.write('REM {fn} {vn} {dt}\n'.format(fn=MYFNAME,vn=MYVERSION,dt=NOW))
			f.write('REM cd /d "%s"\n' % MYPATH)
			f.write('python {mf} 1> {mf}_stdout.log 2> {mf}_stderr.log\n'.format(mf=os.path.split(MYFILE)[1]))
			f.close()

def get_filelist(root, patterns='*', single_level=False, yield_folders=False):
	"""
	List files and directories
	import fnmatch, os
	"""
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

def execute_sql(script_path, database_path):
	"""
	import sqlite3
	"""
	qry = open(script_path, 'r').read()
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	c.executescript(qry)
	conn.commit()
	c.close()
	conn.close()


def db_execute_query2(db_path, query):
	""" execute query in string format """
	""" import sqlite3 """

	if DEBUG:
		print '--- --> Execution de la requête'
		print query

	conn = sqlite3.connect(db_path)
	c    = conn.cursor()
	c.executescript(query)
	conn.commit()
	c.close()
	conn.close()


def db_execute_query(db_path, query):
	""" execute query in string format """
	""" import sqlite3 """

	if DEBUG:
		print '--- --> Execution de la requête'
		print query

	conn = sqlite3.connect(db_path)
	c    = conn.cursor()
	c.execute(query)
	return c.fetchall()


def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM biblio WHERE md5=?", (md5,))

    rows = cur.fetchall()

    for row in rows:
        print(row)


def get_size_in_bytes(file):
	"""
	get file size in bytes
	import os
	"""
	st = os.stat(file)
	return st.st_size


def get_size_in_HR(size,precision=2):
	"""
	Get Human Readable size
	@usage   get_size_in_HR(get_size_in_bytes(file), 2)
	"""
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


def md5func(fname):
	"""
	import hashlib
	"""
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()


def get_size(filename):
	"""
	import os
	"""
	return os.path.getsize(filename)


def db_recup_data(db_path, query):
	"""
	return : list (of tuples)
	"""

	if DEBUG: print '--- --- --> Executing query (return data from db)'

	conn = sqlite3.connect(db_path)
	c    = conn.cursor()
	rule = c.execute(query)
	return [x for x in rule]




def main():
	global EXT_EBO, DB_PATH, TBL_NAME
	tee_autoexec()

	# get extensions to keep and to delete
	kp = EXT_EBO + EXT_SUB + EXT_VID
	dl = EXT_DOC + EXT_EXTRA + EXT_NET + EXT_PIC
	ext_keep, ext_del = get_extension(kp, dl)

	# get filelists
	flist_del  = [ x for x in get_filelist(MYPATH, ext_del,  single_level=True, yield_folders=False)]
	flist_keep = [ x for x in get_filelist(MYPATH, ext_keep, single_level=True, yield_folders=False)]

	# Interroge DB
	dbname = "myebooks_v5.db"
	if os.name == 'nt' : 
		dbpath = 'Z:\\Dropbox\\LABO-DBX\\myebooks\\%s' % dbname
	else:
		dbpath = '/home/reno/Dropbox/LABO-DBX/myebooks/%s' % dbname
	
	cat_ebo = {}
	content = []
	content2 = []
	mvs = []
	
	max_id = db_execute_query(dbpath, "SELECT max(id) FROM catalogue;")
	tmp_id = max_id[0][0]
	mkdir = []
	
	for ext in EXT_EBO:
		for f in flist_keep:
			if f.endswith(ext):
				# cat_ebo[f] = [newfname, fname, verb, sst, genre, tags, auteur, editeur, annee, num_ver_ed, isbn_barcode, pages, fait, md5, size_bytes] 
				fname = f.split(SLASH)[-1]
				md5sum = md5func(f)
				size = str(get_size(f))
				newfname = None
				
				qry = '\
				SELECT \
					   [catalogue].[id],\
					   [catalogue].[verbatim], \
					   [catalogue].[sous_titre], \
					   [catalogue].[genre], \
					   [catalogue].[tags], \
					   [catalogue].[auteur], \
					   [catalogue].[editeur], \
					   [catalogue].[num_ver_ed], \
					   [catalogue].[annee], \
					   [catalogue].[isbn_barcode], \
					   [md5sum].[pages], \
					   [md5sum].[md5], \
					   [md5sum].[size] \
				FROM   [catalogue], [md5sum] \
				WHERE  [md5sum].[cat_id] = [catalogue].[id] \
				AND    [md5sum].[md5] like "%s";' % md5sum
				  
				answer = db_execute_query(dbpath, qry)
				
				#question_pour_db.append(fname, md5sum, size, qry,))
				if answer:
					print "[ 0635 ] ... ", fname, answer
				else:
					print "[ 0635 ] ... -NO HIT- ", fname
				
				row = 2
				
				# answer[0][0] --> id
				# answer[0][1] --> verbatim
				# answer[0][2] --> sous_titre
				# answer[0][3] --> genre
				# answer[0][4] --> tags
				# answer[0][5] --> auteur
				# answer[0][6] --> editeur
				# answer[0][7] --> num_ver_ed
				# answer[0][8] --> annee
				# answer[0][9] --> isbn_barcode
				# answer[0][10] -> pages
				# answer[0][11] -> md5
				# answer[0][12] -> size
				if answer != [] :
									
					genre = answer[0][3] if answer[0][3] != None else ''
					verb  = answer[0][1] if answer[0][1] != None else ''
					sst   = answer[0][2] if answer[0][2] != None else ''
					tags  = answer[0][4] if answer[0][4] != None else ''
					num   = answer[0][7] if answer[0][7] != None else ''
					auteur = answer[0][5] if answer[0][5] != None else ''
					editeur = answer[0][6] if answer[0][6] != None else ''
					pages = answer[0][10] if answer[0][10] != None else 0
					ext = os.path.splitext(fname)[-1]
					
					annee = "%04i" % time.strptime(str(answer[0][8]), "%d/%m/%Y")[0] if str(answer[0][8]) != 'None' else 'xxxx'
					mois  = "%02i" % time.strptime(str(answer[0][8]), "%d/%m/%Y")[1] if str(answer[0][8]) != 'None' else 'xx'
					jour  = "%02i" % time.strptime(str(answer[0][8]), "%d/%m/%Y")[2] if str(answer[0][8]) != 'None' else 'xx'
					date = "%s-%s-%s" % (annee, mois, jour)
					
					# Renaming mask
					if genre == 'BD':
						# BD : {verb}.T{num_ver_ed}.{sous_titre}.{date}.{ext}
						newfname = "{v}.T{n}.{s}{x}".format(v=verb, n="%02i" % int(num), s=sst, d=date, x=ext)
						mkdir.append('faits/BD/"%s"' % verb.upper())
						
					elif genre == 'Livre':
						# Livre : {tags}.{year}.{verb}.{sous_titre}.{editeur}.[pages].{ext}
						# # nfname = [tag]_year_verb_sst_edR_[pg].ext
						newfname = "[{tg}]_{an}_{vb}_{st}_{edR}_[{pg}p].{ex}".format(\
							vb=verb[:51], nm=num, st=sst[:51], an=annee, pg="%03i" % pages, \
							ex=ext, tg="][".join(tags.upper().split(",")), edR=editeur )
	
					elif genre == 'Magazine':
						# MAG : verb_num_sst_annee.ext
						newfname = "{vb}_{nm}_{st}_{d}.{ex}".format(vb=verb[:51], nm="%03i" % int(num), st=sst[:51], d=date, ex=ext)
					
					if newfname:
						newfname = newfname.replace(' ', '.')
						newfname = newfname.replace('__', '_')
						newfname = newfname.replace("'", ".")
						newfname = newfname.replace("..", ".")
						
						if genre == 'BD':
							newfname = "%s/%s" % (verb.upper(), newfname)

						msg = '### %02i ###\n' % len(mvs)
						msg+= 'orig="{oldf}"\n'.format(oldf=fname)
						msg+= 'newf="{newf}"\n'.format(newf=newfname)
						msg+= 'dest="faits/{genre}/$newf"\n'.format(oldf=fname, genre=genre.upper(), newf=newfname)
						msg+= 'if [ -f "$dest" ]; then\n'
						msg+= '    dest="doublons/$newf"\n'
						msg+= '    if [ -f "$dest" ]; then\n'
						msg+= '        dest="$newf"\n'
						msg+= '    fi\n'
						msg+= 'fi\n'
						msg+= 'mv -nv "$orig" "$dest"\n'
						
						mvs.append(msg)
						
				else:
					row += 1
					tmp_id += 1

					header  = "##Table : md5sum;Last id : %s\n" % max_id[0][0]
					header += "form1;comment;cat_id;pages;size;md5\n"
					formula = '="insert into md5sum (comment,cat_id,pages,size,md5) values ("&char(34)&b{row}&char(34)&","&c{row}&","&d{row}&","&char(34)&e{row}&char(34)&","&char(34)&f{row}&char(34)&")"&char(59)'.format(row=row)
					content.append('%s;%s;%s;Null;%s;%s' % (formula, fname, tmp_id, size, md5sum))
					#print "[ 0628 ] ... len content", len(content)
					
					header2  = "##Table : catalogue\n"
					header2 += "form2; fname; id; verbatim; sous_titre; genre; tags; auteur; editeur; num_ver_ed; annee; isbn_barcode\n"
					content2.append('%s;%s;;Null;Null;Null;Null;Null;Null;Null;Null' % (fname, tmp_id))
	
	tmp_content = []
	if content and content2:
		row = len(content2) + 6
		for c in content2:
			# form2 = '="insert into catalogue (id,verbatim,sous_titre,genre,tags,auteur,editeur,num_ver_ed,annee,isbn_barcode) values ("& \
			# c{r}&","& \
			# if(d{r}=\"Null\"; d{r}; char(34)&d{r}&char(34)) &","& \
			# if(e{r}=\"Null\"; e{r}; char(34)&e{r}&char(34)) &","& \
			# if(f{r}=\"Null\"; f{r}; char(34)&f{r}&char(34)) &","& \
			# if(g{r}=\"Null\"; g{r}; char(34)&g{r}&char(34)) &","& \
			# if(h{r}=\"Null\"; h{r}; char(34)&h{r}&char(34)) &","& \
			# if(i{r}=\"Null\"; i{r}; char(34)&i{r}&char(34)) &","& \
			# j{r} &","& \
			# if(k{r}=\"Null\"; k{r}; char(34)&k{r}&char(34)) &","& \
			# if(l{r}=\"Null\"; l{r}; char(34)&l{r}&char(34)) &")"& char(59)'.format(r=row)
			form2 = '="insert into catalogue (id,verbatim,sous_titre,genre,tags,auteur,editeur,num_ver_ed,annee,isbn_barcode) values (" & c{r} & "," & char(34) & d{r} & char(34) & "," & char(34) & e{r} & char(34) & "," & char(34) & f{r} & char(34) & "," & char(34) & g{r} & char(34) & "," & char(34) & h{r} & char(34) & "," & char(34) & i{r} & char(34) & "," & j{r} & "," & char(34) & k{r} & char(34) & "," & char(34) & l{r} & char(34) & ")" & char(59)'.format(r=row)
			
			row += 1
			tmp_content.append('%s;%s' % (form2, c))
			
	
	if content or content2:
		with open('%s_results_DB5.csv' % NOW, 'w') as f:
			f.write(header)
			f.write('\n'.join(content))
			f.write('\n\n')
			f.write(header2)
			f.write('\n'.join(tmp_content))
			f.close()
		
	if mvs:
		with open('%s_moves.sh' % NOW, 'w') as g:
			g.write('#! /usr/bin/env sh\n')
			g.write('mkdir -pv faits/BD faits/MAGAZINE faits/LIVRE doublons 2>/dev/null\n')
			if mkdir:
				g.write('mkdir -pv ' + ' '.join(anti_doublons(mkdir)) + ' 2>/dev/null\n')
			g.write('\n')
			g.write('\n'.join(mvs))
			g.write('\n')
			# g.write('rmdir -v faits/BD/* 2>/dev/null\n')
			# g.write('rmdir -v faits/BD 2>/dev/null\n')
			# g.write('rmdir -v faits/MAGAZINE 2>/dev/null\n')
			# g.write('rmdir -v faits/LIVRE 2>/dev/null\n')
			# g.write('rmdir -v doublons 2>/dev/null\n')
			g.write('find faits/ -type d -empty -delete -print0\n')
			g.close()	
	
	#  [(u'Linux User & Developer', u'Secure your system', u'Magazine', None, None, None, u'01/07/2016', 167, u'2041-3270', 100, 1, u'1da46058759e4d45bdaca956391521fe', 32807266)]

	# cat_ebo[f] = '%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s' % (rowid,fname,verb,sst,genre,tags,auteur,ed,date,num,isbn,pages,fait,md5,size,nfname,mv,row)

	# with open('results_DB4_%s.csv' % NOW, 'w') as f:
		# f.write("db4_master4;fname;verb;sst;genre;tags;auteur;editeur;annee;num_ver_ed;isbn_barcode;pages;fait;md5;size_bytes;newfname;mv;select * from %s where \n" % TBL_NAME)
		# f.write("\n".join(anti_doublons(cat_ebo.values(),sort=True)))
		# f.close()

	# with open('update_move_%s.sh' % NOW, 'w') as g:
		# g.write('#! /usr/bin/env sh\n')
		# g.write('mkdir -pv faits/BD faits/MAGAZINES faits/LIVRES 2>/dev/null\n')
		# g.write('\n'.join(mv_msg))
		# g.write('rmdir -v faits/BD 2>/dev/null\n')
		# g.write('rmdir -v faits/MAGAZINES 2>/dev/null\n')
		# g.write('rmdir -v faits/LIVRES 2>/dev/null\n')
		# g.close()


##################################################################
#### B O D Y           ###########################################
##################################################################

main()

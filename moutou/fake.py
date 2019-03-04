#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......moutou_fake
#EXT.......py
#MAJOR....6
#MINOR....4
#DESCR....produit un log qui simule l'action de moutou (basé sur moutou_v5.1.py)
#USAGE....moutou_v*.py

"""
NOTE DE VERSION --- PENSER A CHANGER $MYFNAME etc.
2018-10-17 v6.4   Now writes a *.sh to update *.ini
2018-09-25 v6.3   Add logging
2018-06-29 v6.2   Fix *.ini that resets after fake run -- resets no more
2017-11-03 v6.0   Ajout option version et autre
2017-10-23 v5.1 

"""

import os, sys, time

MYFNAME   	= "moutou_fake"
MYVERSION 	= "v6.4"
MYEXT		= ".py"
MYDESCR		= "produit un log qui simule l'effet de moutou (basé sur moutou_v5.1.py)"
MYUSAGE		= "$ python {fn} OPTION".format(fn=os.path.basename(os.path.abspath(__file__)))

MYPATH = os.path.dirname(os.path.abspath(__file__))
MYFILE = os.path.abspath(__file__)


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
		
NOW    = time.strftime("%Y-%m-%d_%H%M%S")
SLASH  = os.sep
NL     = os.linesep

AUTOEXEC = os.path.join(MYPATH, '%s_%s_autoexec.bat' % (MYFNAME, MYVERSION))


print '***********************'
print '**** DEBUG IS %s  ****' % ('ON ' if DEBUG else 'OFF')
print '***********************'
msg = 'EXECUTION DE %s %s %s\nLOCALISATION %s' % (MYFNAME, MYVERSION, NOW, MYFILE)
print msg
print '.' * (len(msg) / 2 )

sys.path.append(MYPATH + SLASH + 'moutou-settings')
#sys.path.append('Z:\\Dropbox\\LABO-DBX\\moutou-modul\\moutou-settings')
from moutou_fonctions import *

##################################################################
#### F O N C T I O N S ###########################################
##################################################################

def main_fake():
	global EXTENSION_ALL, CFRAM_mouh
	
	# GENERATION DE L'AUTOEXEC.BAT
	tee_autoexec(AUTOEXEC, MYPATH, MYFNAME, MYVERSION, MYFILE)
	
	# GET EXTENSIONS OF FILES TO KEEP AND TO DELETE
	kp = EXT_EBO + EXT_SUB + EXT_VID
	dl = EXT_DOC + EXT_EXTRA + EXT_NET + EXT_PIC
	ext_keep, ext_del = get_extension(kp, dl)
	
	# GET FILELISTS
	# flist : ['F:\\path\\to\\file.mp4']
	if DEBUG and not DEBUG2:
		flist_keep = [ x.replace('\n', '').replace('\r', '') for x in open(FKEEP_DEBUG, 'r')]
		flist_del =  [ x.replace('\n', '').replace('\r', '') for x in open(FDEL_DEBUG, 'r')]
	else:
		flist_del  = [ x for x in get_filelist(MYPATH, ext_del,  single_level=False, yield_folders=False)]
		flist_keep = [ x for x in get_filelist(MYPATH, ext_keep, single_level=False, yield_folders=False)]
	
	if not flist_keep : 
		build_robocop()
		print empties(MYPATH)
		sys.exit("Il n'y a pas de fichiers à déplacer. Bye !")

	# GET DATA RENAMING  
	# data_mouh : [(sSearch, sReplacewith, sComment)] 
	# data_mouh : [ "('Ma.Ag.Sh', 'Marvels.Agents.of.SHIELD')", # Marvel Agent of SHIELD ]
	data_mouh  = parse_renaming_rules(CFRAM_mouh)
	data_mouh += [(x, '') for x in ELEMENTS_REN]
	data_mouh = clean_special(data_mouh)
	data_mouh = anti_doublons(data_mouh, sort=True)
	if DEBUG2: 
		print "0113 ... avant ",flist_del

	# CLEAN FLIST
	# flist : ['F:\\path\\to\\file.mp4']	
	flist_del, flist_keep = clean_flist(flist_del, flist_keep, data_mouh)
	if DEBUG2:
		print "0117 ... apres ",flist_del
	
	# READ & AMEND INI FILE
	inst = IniMaker()
	inst.read_ini()
	inst.parse_ini()

	# GET DATA CATEGORY
	# data series : ['American.Crime.Story']
	# data films  : ['Fury.2010']
	# data_tv     : ['La.vie.secrete']
	# RAPPEL :
	# DATA_TRAILERS =  ['trailer', 'promo', 'clip', 'spot', 'teaser', 'featurette']
	# data_ebooks = []
	data_series = anti_doublons(read_file(CFRAM_series, trigger=True))
	data_films  = anti_doublons(read_file(CFRAM_films,  trigger=True))
	data_tv	    = anti_doublons(read_file(CFRAM_tv,     trigger=True))
	data_jan    = anti_doublons(read_file(CFRAM_jan,    trigger=True))
	
	big_data = get_big_data(data_films, data_series, data_tv, data_jan)
	
	log = ScriptMaker()
	logname = "moutou_%s_%s_FAKE.log" % (MYVERSION, NOW)
	
	for file in flist_keep:
	
		nfile = NewfileMaker(file)
		nfile.get_newfname(data_mouh)
		nfile.extension = os.path.splitext(file)[1]

		#cat.add(file, [nfile.oldpath, nfile.oldfname, nfile.oldpath, '', nfile.newfname, 'unk', True, True])
		nfile.flag = 'unk'
		nfile.check_presence()

		# DETECTER FILMS, SERIES, TV & UNKNOWN
		nfile.detect_general(big_data)
				
		# DETECTER LES EBOOKS
		nfile.detect_ebooks()
			
		# DETECTER LES TRAILERS
		nfile.detect_trailers()

		# TODO DETECTER JUNK APRES NEWFNAME

		# CLOSE DEAL
		nfile.check_presence()
		nfile.get_action()
		
	# DETECTER LES DOUBLONS 2
	detect_doublons_wide(flist_keep)

	# PRODUIT LE LOG
	head = [\
		"# Log donnant un aperçu de l'effet de moutou",
		'# Produit par %s %s @ %s' % (MYFNAME, MYVERSION, MYFILE),
		'# Execution du %s' % NOW,
		"# DEBUG is %s" % ("ON" if DEBUG else "OFF"),
		'#' + "="*50]	

	tmp_lmove=[]
	if LIST_MOVE:
		for tup in LIST_MOVE:
			tmp_lmove.append('mv -nv "%s" "%s"' % (tup[0], tup[1]))
			
	tmp_lmd = []
	if LIST_MKDIR:
		for x in LIST_MKDIR:
			tmp_lmd.append('mkdir -pv "%s"' % x)
		
	body = ["\n# DOUBLONS\n# --------"]
	body += LIST_DOUBLONS
	body += ["\n# MKDIR\n# --------"]
	body += tmp_lmd
	body += ["\n# MOVE\n# --------"]
	body += tmp_lmove
	body += ["\n# INCONNUS\n# --------"]
	body += LIST_UNKNOWNS
	
	foot = ['\n\n# UPDATE\n# --------\ncat > %s << DELIM\n[TV]\n\n\n[SERIES]\n\n\n[FILMS]\n\n\nDELIM' % ININAME]
	
	log.writeScript(logname, head, body, foot)
	
	display_lists()
	
	if DEBUG2: 
		print "LIST_DEL : ", LIST_DEL
		print "flist_del: ", flist_del

	# if LIST_UNKNOWNS:
		# script = ScriptMaker()
		# script_name = "moutou_%s_%s_UPDATE_INI.sh" % (MYVERSION, NOW)
		# script_head = ["#!/usr/bin/env sh"]
		# script_body = ["# Script pour mettre à jour *.ini\n"]
		# script_body+= ["# INCONNUS AU BATAILLON :"]
		# script_body+= ["# -----------------------"]
		# for inc in LIST_UNKNOWNS:
			# script_body.append('# ' + inc)
		
		# script.writeScript(script_name, script_head, script_body, foot)
		
	if LIST_UNKNOWNS:
		script = ScriptMaker()
		script_name = "scr_FAKE_UPDATE_LST_%s.sh" % NOW
		
		script_head = ["#!/usr/bin/env sh"]
		
		script_body = ["# Script pour mettre à jour *.ini"]
		script_body+= ["# Notes:"]
		script_body+= ["# Comment line   : CTRL-K"]
		script_body+= ["# Uncomment line : CTRL-SHIFT-K\n"]
		script_body+= ["# INCONNUS AU BATAILLON :"]
		script_body+= ["# -----------------------"]
		for inc in LIST_UNKNOWNS:
			script_body.append('# ' + inc)
		
		script_foot = ["\n## SERIES :"]
		script_foot+= ["## --------"]
		script_foot+= ['# cat >> "%s" << DELIM' % CFRAM_series]
		script_foot+= ["\n\n\n# DELIM\n"]
		script_foot+= ["## FILMS :"]
		script_foot+= ["## ------"]
		script_foot+= ['# cat >> "%s" << DELIM' % CFRAM_films]
		script_foot+= ["\n\n\n# DELIM\n"]
		script_foot+= ["## JAN :"]
		script_foot+= ["## -----"]
		script_foot+= ['# cat >> "%s" << DELIM' % CFRAM_jan]
		script_foot+= ["\n\n\n# DELIM\n"]
		script_foot+= ["## TV :"]
		script_foot+= ["## ----"]
		script_foot+= ['# cat >> "%s" << DELIM' % CFRAM_tv]
		script_foot+= ["\n\n\n# DELIM\n"]
		
		script.writeScript(script_name, script_head, script_body, script_foot)

##################################################################
#### M A I N           ###########################################
##################################################################
import logging
try:
	main_fake()

except Exception as err :
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)

	# create a file handler
	handler = logging.FileHandler(os.path.join(MYPATH, '%s_%s_error_%s.log' % (MYFILE, MYVERSION,NOW)))
	handler.setLevel(logging.INFO)

	# create a logging format
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)

	# add the handlers to the logger
	logger.addHandler(handler)

	logger.info(err)

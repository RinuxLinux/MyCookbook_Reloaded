#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......moutou
#EXT.......py
#MAJOR....6
#MINOR....7
#DESCR....script python pour trier Mouh-x + renommage (move-tout_v7.0.20161111)
#USAGE....moutou_v*.py

"""
NOTE DE VERSION --- PENSER A CHANGER $MYFNAME etc.
2018-12-22 v6.7   traitement special fname DROLEMENT BETE
2018-11-25 v6.6   Reintro de parse txt to nfo
2018-11-09 v6.5   Minor fixes through vim
2018-09-25 V6.4   Add logging
2018-02-13 v6.3   Changement nom de fichier (titmou pour TITAN; satmou pour SATELLITE etc)
2017-11-17 v6.2   Minor fixes ('Marvels' new dir) 
2017-11-12 v6.1   Ajout rewrite_cfram_mouh()
2017-11-10 v6.0   Fonctions à part
2017-11-02 v5.2   Amelioration build_robocop(): meilleur output
"""

##################################################################
#### S E T U P         ###########################################
##################################################################

import os, sys, time
import re # special Mini-Loup
from parse_txt_to_nfo import main as main_parse

MYFNAME   	= "moutou_titan"
MYVERSION 	= "v6.7"
MYEXT		= ".py"
MYDESCR		= "moutou v6+ : fonctions sont dans un module externe"
MYUSAGE		= "$ python %s [ OPTION ]" % os.path.basename(os.path.abspath(__file__))

MYFILE = os.path.abspath(__file__)
MYPATH = os.path.dirname(os.path.abspath(__file__))
SLASH  = os.sep

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

AUTOEXEC = os.path.join(MYPATH, '%s_%s_autoexec.bat' % (MYFNAME, MYVERSION))
NOW    = time.strftime("%Y-%m-%d_%H%M%S")

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

def main_moutou():

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
		
	if DEBUG2:
		print "[ SETUP-- @0104 ] ... %03i files in flist_keep" % len(flist_keep)
		print "[ SETUP-- @0104 ] ... %03i files in flist_del" % len(flist_del)
		
	if not flist_keep :
		build_robocop(MYPATH, MYFNAME, MYVERSION, MYFILE)
		print empties(MYPATH)
		sys.exit("Il n'y a pas de fichiers à déplacer. Bye !")

	# GET DATA RENAMING
	# data_mouh : [(sSearch, sReplacewith, sComment)]
	# data_mouh : [ "('Ma.Ag.Sh', 'Marvels.Agents.of.SHIELD')", # Marvel Agent of SHIELD ]
	data_mouh  = parse_renaming_rules(CFRAM_mouh)
	data_mouh += [(x, '') for x in ELEMENTS_REN]
	data_mouh = clean_special(data_mouh)
	data_mouh = anti_doublons(data_mouh, sort=True)
	
	# CLEAN FLIST
	# flist : ['F:\\path\\to\\file.mp4']
	flist_del, flist_keep = clean_flist(flist_del, flist_keep, data_mouh)
	
	# READ & AMEND INI FILE
	inst = IniMaker()
	inst.iniProcess()

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

        # PROCESSING (or not)
        if not DEBUG:
		process(big_data, flist_del, MYFNAME, MYVERSION, MYFILE)
	else:
		process_fake(big_data, flist_del, MYFNAME, MYVERSION, MYFILE)
        
	
        # REWRITE CFRAM_mouh
	rewrite_cfram_mouh()
       
        for lst in [ CFRAM_series, CFRAM_films, CFRAM_jan, CFRAM_tv ] :
            rewrite_lst(lst)

        # Clean EMPTIES
        # empties("G:\\_TMP_kodi")
        print empties(MYPATH)
       
        # Build ROBOCOP.BAT
	build_robocop(MYPATH, MYFNAME, MYVERSION, MYFILE)
	

##################################################################
#### M A I N           ###########################################
##################################################################


main_parse
main_moutou()

#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......moutou_build_robocop
#EXT.......py
#MAJOR....6
#MINOR....0
#DESCR....produit un log qui simule l'action de moutou (basé sur moutou_v5.1.py)
#USAGE....moutou_build_robocop.py OPTION

"""
NOTE DE VERSION --- PENSER A CHANGER $MYFNAME etc.
2017-11-11 v6.0   Proper new function-less module
2017-11-02 v5.2   meilleur output pour build_robocop()
2017-10-23 v5.1 

"""

import sys, time, os


MYFNAME   	= "moutou_build_robocop"
MYVERSION 	= "v6.0"
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
#### M A I N           ###########################################
##################################################################

tee_autoexec(AUTOEXEC, MYPATH, MYFNAME, MYVERSION, MYFILE)
build_robocop(MYPATH, MYFNAME, MYVERSION, MYFILE)
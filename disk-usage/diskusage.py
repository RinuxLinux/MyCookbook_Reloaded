#!/usr/bin/env python
#-*- coding: utf-8 -*-
#NOM......diskusage.py
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....Get disk usage with os.stat (LINUX only)
#USAGE....diskusage.py PATH

"""
NOTE DE VERSION --- PENSER A CHANGER $MYFNAME etc.
2018-03-14 v1.0   Premier jet 
"""
##################################################################
#### S E T U P         ###########################################
##################################################################

import os, sys, time

MYFNAME   	= "diskusage"
MYVERSION 	= "v1.0"
MYEXT		= ".py"
MYDESCR		= "Get disk usage with os.stat (LINUX only)"
MYUSAGE		= "$ python {fn} [ PATH | OPTION ]".format(fn=os.path.basename(os.path.abspath(__file__)))

MYFILE = os.path.abspath(__file__)
MYPATH = os.path.dirname(os.path.abspath(__file__))
SLASH  = os.sep

#=============#
DEBUG  = False
DEBUG1 = False   # debug + detaillé
DEBUG2 = False   # ?
#DEBUG  = True
#=============#

LDC = sys.argv[1:]
ldc = [x.upper() for x in LDC]

if 'DEBUG2' in ldc:
	DEBUG = True
	DEBUG1 = True
	DEBUG2 = True

elif 'DEBUG1' in ldc:
	DEBUG  = True
	DEBUG1 = True

elif 'DEBUG' in ldc:
    DEBUG  = True
	
if 'VERSION' in ldc:
	sys.exit("--> %s %s" % (MYFNAME, MYVERSION))

if 'USAGE' in ldc:
	msg = ["USAGE"]
	msg+= ["     $ python {mf}".format(mf=os.path.basename(MYFILE))]
	msg+= ["OPTIONS"]
	msg+= ["     'debug'     debuggage simple"]
	msg+= ["     'debug1'    debuggage détaillé"]
	msg+= ["     'debug2'    utilisation de la vraie flist"]
	msg+= ["     'usage'     affiche ce message"]
	msg+= ["     'version'   affiche fname et version"]
	sys.exit("\n".join(msg))

AUTOEXEC = os.path.join(MYPATH, '%s_%s_autoexec.bat' % (MYFNAME, MYVERSION))
NOW = time.strftime("%Y-%m-%d_%H%M%S")

##################################################################
#### F O N C T I O N S ###########################################
##################################################################

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


def disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return total, used, free

def main():
    # parse ldc
	options = []
	disque = MYPATH
	for x in LDC:
		if x.upper() in ['DEBUG', 'DEBUG1', 'VERSION', 'USAGE']:	
			option.append(x.upper())
		elif os.path.isdir(x):
			disque = x
	
	total, used, free = disk_usage(disque)
	percent_used = used * 100 / total	
	total_HR = get_size_in_HR(total,precision=2)
	used_HR  = get_size_in_HR(used,precision=2)
	free_HR  = get_size_in_HR(free,precision=2)

	len_max = max([len(total_HR), len(disque), len(used_HR), len(free_HR)])
	sp1 = len_max * ' '
	sp2 = (len_max - len(total_HR)) * ' '
	sp3 = (len_max - len(used_HR)) * ' '
	sp4 = (len_max - len(free_HR)) * ' '
#	print("%s | total %s | used %s | free %s | used %s%%" % (disque, total_HR, used_HR, free_HR, percent_used))
	print("%s \n--> total %s \n--> used  %s \n--> free  %s \n--> used  %s%%" % (disque, total_HR, used_HR, free_HR, percent_used))

main()









# BRANCHEMENT QUAND TOUS LES TESTS PRÉCÉDENTS ONT ECHOUÉ
#echo "..ERREUR..\033[1m$1\033[0m n'est pas une option valide." && echo $USAGE && exit 1


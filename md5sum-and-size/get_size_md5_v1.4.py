#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......get_size_md5
#EXT.......py
#MAJOR....1
#MINOR....4
#DESCR....write fname, size and md5sum of ebooks into a .cvs
#USAGE....get_size_md5.py
MYFNAME   	= "get_size_md5"
MYVERSION 	= "v1.4"
MYEXT		= ".py"
MYDESCR		= "write fname, size and md5sum of ebooks into a .cvs"
MYUSAGE		= "$ python {fn}_{vn}{ext}".format(fn=MYFNAME,vn=MYVERSION,ext=MYEXT)

'''
NOTE DE VERSION
2017-08-21 v1.4   change output
2017-08-19 v1.3   Add column for db update 
2017-08-18 v1.2   Add separator ";" for output
2017-08-16 v1.1   Proper presentation
'''
import os, sys
import time
import fnmatch
import hashlib

MYPATH = os.path.dirname(os.path.abspath(__file__))
MYFILE = os.path.abspath(__file__)

if os.name == "posix":
	sys.exit("Script non adapté pour UNIX. Revoir code source @ %s" % MYFILE) 

NOW = time.strftime("%Y-%m-%d_%H%M%S")
SLASH = os.sep
AUTOEXEC = os.path.join(MYPATH, '%s_%s_autoexec.bat' % (MYFNAME, MYVERSION))
CSV_NAME = 'get_size_md5_%s.csv' % NOW

ext_ebooks = ['.pdf', '.cbr', '.cbz', '.epub']
mypaths = [MYPATH]
#mypaths = ['F:\\EBOOKS-F1\\=trier=', 'F:\\EBOOKS-F1\\=trier=\\faits']


##############################################

def get_filelist(root, patterns='*', single_level=False, yield_folders=False):
	'''
	List files and directories
	usage: lstdir = list(get_filelist(str_path, "*.jpg;*.png")
	import os, fnmatch
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


def tee_autoexec():
	""" Creer le fichier .bat qui permet d'executer le script en loggant stderr/out """
	global AUTOEXEC, MYPATH
	if not os.path.isfile(AUTOEXEC) and os.name == "nt":
		with open(AUTOEXEC, 'w') as f:
			f.write('REM cd /d "%s"\n' % MYPATH)
			f.write('{fn}_{vn}{ext} 1> {fn}_{vn}_stdout.log 2> {fn}_{vn}_stderr.log\n'.format(fn=MYFNAME,vn=MYVERSION,ext=MYEXT))
			f.close()


def fix_extensions_list(list_of_extensions):
	ext_fixed = []
	for ext in list_of_extensions:
		ext_fixed.append('*' + ext)
	return ext_fixed


def md5(fname):
	"""
	import hashlib
	"""
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()


def main():
	global mypaths, MYPATH, SLASH, CSV_NAME

	filelist = []
	for mypath in mypaths:
		filelist += list(get_filelist(mypath, ';'.join(fix_extensions_list(ext_ebooks)), single_level=True, yield_folders=False))

	msg = ['update TEXT;filename TEXT;verbatim TEXT;sous_titre TEXT;genre TEXT;tags TEXT;auteur TEXT;editeur TEXT;annee TEXT;num_ver_ed INT;ISBN_barcode TEXT;pages INT;Fait INT;md5 TEXT;size_bytes INTEGER; id INT; newname TEXT; mv TEXT']
	tblname = "tri160517"
	updoot=[]
	form1=[]
	form2=[]
	format_annee = "jj/mm/aaaa"
	form_day = "jj"
	form_mon = "mm"
	form_yea = "aaaa"
	#{fy}-{fm}-{fd}
	#{fd}/{fm}/{fy}
	#fy=form_year,fm=form_mon,fd=form_day
	i=2
	for file in filelist:
		filename = file.split(SLASH)[-1]
		size = os.path.getsize(file)
		md5sum = md5(file)
		# INSERT OR REPLACE  INTO tri160517 VALUES ("Electronique_UIT 1ere Annee_2017_id0543,pdf","Electronique","UIT 1ere Annee","Livre","electronique","Duveau J","Dunod","01/01/17",2,"978-2-10-076447-1",272,1,"d9fd7e8630000b9498d1656e43de4637",11132803);
		#update = '="INSERT INTO {tn} VALUES ("&char(34)&"{fn}"&char(34)&",Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,Null,"&char(34)&"{md5}"&char(34)&",{sz});"'.format(tn=tblname,fn=filename,md5=md5sum,sz=size) 
		#update = 'INSERT INTO {tn} (filename, verbatim, genre, md5, size_bytes) VALUES (\"\"{fn}\"\", "\"\Canard PC Hardware\"\", \"\"Magazine\"\", \"\"{md5}\"\", {sz})'.format(tn=tblname,fn=filename,md5=md5sum,sz=size)
		
		formule_newfname = '=SUBSTITUTE(C{inc}&"_"&TEXT(J{inc};"000")&"_"&D{inc}&"_"&TEXT(I{inc};"{fy}-{fm}-{fd}")&"_id"&TEXT(P{inc};"0000")&".pdf";" ";".")'.format(inc=i,fy=form_yea,fm=form_mon,fd=form_day)
		
		form_mv = '="mv -nv "&CHAR(34)&B{inc}&CHAR(34)&" "&CHAR(34)&Q{inc}&CHAR(34)'.format(inc=i)
		
		update = '="INSERT OR REPLACE  INTO {tn} VALUES ("&IF(ISBLANK(B{inc});"Null";CHAR(34)&B{inc}&CHAR(34))&","&IF(ISBLANK(C{inc});"Null";CHAR(34)&C{inc}&CHAR(34))&","&IF(ISBLANK(D{inc});"Null";CHAR(34)&D{inc}&CHAR(34))&","&IF(ISBLANK(E{inc});"Null";CHAR(34)&E{inc}&CHAR(34))&","&IF(ISBLANK(F{inc});"Null";CHAR(34)&F{inc}&CHAR(34))&","&IF(ISBLANK(G{inc});"Null";CHAR(34)&G{inc}&CHAR(34))&","&IF(ISBLANK(H{inc});"Null";CHAR(34)&H{inc}&CHAR(34))&","&IF(ISBLANK(I{inc});"Null";CHAR(34)&TEXT(I2;"{fd}/{fm}/{fy}")&CHAR(34))&","&IF(ISBLANK(J{inc});"Null";J{inc})&","&IF(ISBLANK(K{inc});"Null";CHAR(34)&K{inc}&CHAR(34))&","&IF(ISBLANK(L{inc});"Null";L{inc})&","&IF(ISBLANK(M{inc});"Null";M{inc})&","&IF(ISBLANK(N{inc});"Null";CHAR(34)&N{inc}&CHAR(34))&","&IF(ISBLANK(O{inc});"Null";O{inc})&");"'.format(tn=tblname, fy=form_yea,fm=form_mon,fd=form_day, inc=i)
		
		verbatim = ""
		sous_titre =""
		genre = "Magazine"
		msg.append('update;%s;%s;%s;%s;;;;;;;;;%s;%i;0000;substitute;mv' % (filename, verbatim, sous_titre,genre, md5sum,size))
		updoot.append(update)
		form1.append(formule_newfname)
		form2.append(form_mv)
		i+=1
		
		print('%s;%s;%s;%s') % (filename, verbatim, md5sum, size)
		
	print "********\n",  '\n'.join(msg), "\n********\n"
	flux = open(MYPATH + SLASH + CSV_NAME, 'w')
	flux.write('\n'.join(msg))
	flux.close()

	with open(MYPATH + SLASH + "updoot_%s.txt" % NOW, 'w') as f:
		f.write('\n'.join(updoot))
		f.write('\n\n')
		f.write('\n'.join(form1))
		f.write('\n\n')
		f.write('\n'.join(form2))
		f.close()
	
m = 'EXECUTION DE %s %s %s %s' % (MYFNAME, MYVERSION, NOW, MYFILE)
print m
print "=" * len(m)

tee_autoexec()
main()
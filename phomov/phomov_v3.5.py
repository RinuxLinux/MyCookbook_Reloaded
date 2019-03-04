#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......phomov
#EXT.......py
#MAJOR....3
#MINOR....5
#DESCR....photo-move v3 python edition -- pour JAN uniquement
#USAGE....phomov.py
MYFNAME   = 'phomov'
MYVERSION = 'v3.5'

'''
CHANGELOG: !!! PENSER A CHANGER  `MYVERSION`  !!!
2017-07-11 v3.5   Perfect scripts that are produced
2017-07-11 v3.4   Fix get_dest_dirname
2017-07-10 v3.3   Modularisation
2017-07-10 v3.2   Adapte si TOTOR est la SOURCE ou bien DROPBOX
2017-07-10 v3.1   EAFP approche sur shutil.move: "if isfile" remplace par "try except"
2017-07-10 v3.0   Debut
'''

import os, time, sys

MYPATH = os.path.dirname(os.path.abspath(__file__))
AUTOEXEC = os.path.join(MYPATH, '%s_%s_autoexec.bat' % (MYFNAME, MYVERSION))

if os.name == "posix":
    DROPBOX_PATH = '%s/Dropbox' % os.environ['HOME']
    TOTOR_PATH = "/media/%s/Totor/" % os.environ['USER']
elif os.name == 'nt' and os.environ['COMPUTERNAME'].lower() == 'win7-titan':
    DROPBOX_PATH = 'Z:\\Dropbox'
    TOTOR_PATH = "T:\\"
else:
    sys.exit('OS n\'est ni posix, ni NT. PC n\'est pas WIN7-TITAN. Bye!')

if MYPATH.startswith(DROPBOX_PATH):
    DEST_FOLDER = os.path.join(DROPBOX_PATH, 'Camera Uploads', 'JAN')
else:
    DEST_FOLDER = MYPATH





#################################################
def anti_doublons(liste, sort=False):
    '''
    tri les doublons et elimine les elements nuls
    '''
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
    temps = [x for x in time.localtime()]
    yyyy  = '%04i' % temps[0]
    mm    = '%02i' % temps[1]
    dd    = '%02i' % temps[2]
    HH    = '%02i' % temps[3]
    MM    = '%02i' % temps[4]
    SS    = '%02i' % temps[5]
    return '%s-%s-%s_%s%s%s' % (yyyy,mm,dd,HH,MM,SS)

def tee_autoexec():
    """ Creer le fichier .bat qui permet d'executer le script en loggant stderr/out """
    global AUTOEXEC
    if not os.path.isfile(AUTOEXEC) and os.name == "nt":
        with open(AUTOEXEC, 'w') as f:
            f.write('rem cd /d "%s"\n' % os.getcwd())
            f.write('{fn}_{vn}.py 1> {fn}_stdout.log 2> {fn}_stderr.log\n'.format(fn=MYFNAME,vn=MYVERSION))
            f.close()

def exif_info2time(ts):
    """changes EXIF date ('2005:10:20 23:22:28') to number of seconds since 1970-01-01"""
    tpl = time.strptime(ts, '%Y-%m-%d_%H%M%S')
    return time.mktime(tpl)
    
def show_fdt(fdt):
    """human readable format of file modification datetime"""
    return time.strftime("%Y-%m", time.gmtime(fdt))

def get_dest_dirname(filelist):
    """ returns dict with key=fname, values=newpath """
    global DEST_FOLDER
    tmp = {}
    for x in filelist:
        dirname = None
        dimensions = None
        try:
            time        = exif_info2time(x[:17])
            newdir      = show_fdt(time)
            dirname     = os.path.join(DEST_FOLDER, newdir)
            dimensions  = 'x' in x.split('_')[2]
        except:
            pass
        print x, ' --> ', dirname
        if dirname and dimensions:
            tmp[x] = dirname
    return tmp

def build_mkdir_script(dlist):
    """ 
    @arg   takes list of newdirnames
    @ret   returns list of strings (lines of codes)
    """
    md = []
    i=0
    for m in dlist:
        i+=1
        m = m.replace('\\', '\\\\')
        msg = 'try:\n'
        msg+= '\tos.makedirs("%s")\n' % m
        msg+= "\tprint 'Made dir >>> %s'\n" % m
        msg+= "\tlog_msg.append('[ 0x0%03i ] Made dir >>> %s')\n" % (i, m)
        msg+= 'except:\n'
        msg+= '\tpass\n\n'
        md.append(msg)
    return md

def build_mv_script(dict_fname_newpath):
    """ 
    @arg   takes dict {'fname': 'newpath'}
    @ret   returns list of strings (lines of codes)
    """
    global MYPATH

    mv = []
    i=0
    for key in dict_fname_newpath:
        newpath = dict_fname_newpath[key].replace('\\', '\\\\')
        i+=1
        msg = 'try:\n'
        msg+= '\tshutil.move("%s", "%s")\n'   % (os.path.join(MYPATH, key).replace('\\', '\\\\'), newpath)
        msg+= '\tprint "Moved %s --> %s" \n' % (key, newpath)
        msg+= "\tlog_msg.append('[ 0x1%03i ] Moved %s --> %s')\n" % (i, key, newpath)
        msg+= 'except:\n'
        msg+= '\tpass\n\n'
        mv.append(msg)
    return mv

def build_header():
    """
    @arg   None
    @ret   Text for the beginning of the python script
    """
    global NOW
    head = '#!/usr/bin/env python\n'
    head+= '#-*-coding: UTF-8 -*-\n'
    head+= '# phomov_SCRIPT_%s.py\n' % NOW
    head+= '# Usage unique, vers JAN/ uniquement (destination des fichiers)\n\n'
    head+= 'import os, sys\n\n'
    head+= 'try:\n\timport shutil\nexcept Exception as ex:\n\tsys.exit(ex)\n\n'
    head+= "print '!!! WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNI !!!'\n"
    head+= "print '!!!                                                               !!!'\n"
    head+= "print '!!! Usage unique, vers JAN/ uniquement (destination des fichiers) !!!'\n"
    head+= "print '!!!                                                               !!!'\n"
    head+= "print '!!! NG WARNING WARNING WARNING WARNING WARNING WARNING WARNING WA !!!'\n"
    head+= "rep = raw_input('--> Continuer? (Y/n) ... ').lower()\n"
    head+= "if rep != 'y':\n"
    head+= "\tsys.exit('Ok. Bye!')\n\n"
    head+= "log_msg = []\n"
    head+= "log_jnl = 'phomov_SCRIPT_%s.log'\n\n" % NOW
    return head

def build_footer():
    """ 
    @arg   None
    @ret   Text for the end of the script
    """
    global NOW
    foot = "log_msg.sort()\n"
    foot+= "if not log_msg: \n"
    foot+= "\tlog_jnl = 'phomov_SCRIPT_NO_MOVE_%s.log'\n\n" % NOW
    foot+= "with open(log_jnl, 'w') as f:\n"
    foot+= "\tf.write('\\n'.join(log_msg))\n"
    foot+= "\tf.close()\n\n"
    return foot

def write_script(sname, head, mkd, mov, foot):
    with open(sname, 'w') as f:
        f.write(head)
        f.write('\n'.join(mkd))
        f.write('\n'.join(mov))
        f.write(foot)
        f.close()
        
def check_surroundings():
    global MYPATH, DROPBOX_PATH, DEST_FOLDER
    if MYPATH.startswith(DROPBOX_PATH):
        DEST_FOLDER = os.path.join(DROPBOX_PATH, 'Camera Uploads', 'JAN')
    elif MYPATH.startswith(TOTOR_PATH):
        DEST_FOLDER = MYPATH

    if not os.path.isdir(DEST_FOLDER):
        sys.exit('Trouve pas le rep CIBLE: %s' % DEST_FOLDER)
    
    return DEST_FOLDER
    

#################################################

def main():
    global NOW, MYPATH, DEST_FOLDER
    
    # SET UP AUTOLOG (autoexec.bat)
    tee_autoexec()
    
    # GET FILE LIST
    jlist = [x for x in os.listdir(MYPATH) if x.lower().endswith('.jpg')]

    # GET OUT IF NO FILES FOUND
    if not jlist:
        sys.exit("Aucun fichier .jpg ou .JPG n'a ete trouve.")
    
    # GET NEW DNAME
    dict = get_dest_dirname(jlist)   # dict={"fname": "newdname"}

    # BUILD MKDIR TEXT
    dirs = anti_doublons(dict.values())
    md = build_mkdir_script(dirs)
    
    # BUILD MV TEXT
    mv = build_mv_script(dict)
    mv = anti_doublons(mv, sort=True)
    
    # BUILD HEADER OF SCRIPT
    header = build_header()

    # BUILD FOOTER OF SCRIPT
    footer = build_footer()

    # WRITE SCRIPT
    script_name = 'phomov_SCRIPT_%s.py' % NOW
    write_script(script_name, header, md, mv, footer)
    raw_input('Ecriture du script %s terminée. Press Enter to exit.' % script_name.upper())






NOW = get_time()
main()

#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......get_time
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....get actual time for renaming purpose (NOW & convert epoch)
#USAGE....get_time() => str

import time

def get_time():
	NOW = ':'.join(str(x) for x in time.localtime()[:6])
	DATE = '-'.join(['%02i' % int(x) for x in NOW.split(':')[:3]])
	TIME = ''.join(['%02i' % int(x) for x in NOW.split(':')[3:6]])
	TIME2 = ':'.join(['%02i' % int(x) for x in NOW.split(':')[3:6]])
	NOW2 = '%s_%s' % (DATE, TIME)
	epoch = int(time.mktime(time.strptime(NOW2, '%Y-%m-%d_%H%M%S'))) - time.timezone
	return NOW2

'''
print('NOW   %s') % NOW
print('NOW2  %s') % NOW2
print('epoch %s') % epoch
'''

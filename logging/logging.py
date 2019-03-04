#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......logging
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....log message into file that's can be reset if need be
#USAGE....logging(log_file, msg, reset=False) => no return

import os

def logging(log_file, msg, reset=False):
	if reset :
		if os.path.isfile(log_file):
			os.remove(log_file)
	flux = open(log_file, 'a')
	flux.write(msg)
	flux.write('\n')
	flux.close()

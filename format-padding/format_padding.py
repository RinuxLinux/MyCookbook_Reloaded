#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......format_padding
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....prend float pour un padding de precision p
#USAGE....format_pad(n, precision) => str(float)

def format_pad(n, precision): 
	return '%0*i' % (precision, int(n))

	
print type(format_pad(3, 0))
print format_pad(3, 2)
print format_pad(3, 3)

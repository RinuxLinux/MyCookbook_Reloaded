#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#NOM......anti_doublons
#EXT.......py
#MAJOR....1
#MINOR....0
#DESCR....Retourne une liste d'elements uniques d'une liste
#USAGE....anti_doublons(liste, sort=False, case_sensitive=True)

def anti_doublons(liste, sort=False, case_sensitive=True):
	"""
	tri les doublons et elimine les elements nuls
	
	@ver 20180219_1426
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
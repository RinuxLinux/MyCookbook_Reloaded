#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#NOM......anti_doublons
#EXT.......py
#MAJOR....1
#MINOR....1
#DESCR....Retourne une liste d'elements uniques d'une liste
#USAGE....anti_doublons(liste, sort=False, case_sensitive=True)

def anti_doublons(liste, sort=False, case_sensitive=True):
	"""
	Tri les doublons et elimine les elements nuls
	
	@ver   20190325_1700
	@arg   list
	@ret   list sans dups
	"""

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
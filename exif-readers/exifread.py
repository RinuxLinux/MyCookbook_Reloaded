#!/usr/bin/env python
#-*-coding: utf-8 -*-
#NOM......phomov3
#EXT.......py
#MAJOR....3
#MINOR....0
#DESCR....photo move python
#USAGE....phomov3 $DIR_PICS $DIR_CIBLE (jpg assumed)



import exifread
import EXIF


path_name = 'Z:\\Dropbox\\LABO-DBX\\170629_python-exiftool-II\\test.jpg'
# Open image file for reading (binary mode)
f = open(path_name, 'rb')

# Return Exif tags
tags = exifread.process_file(f)

print type(tags)
print tags
#!/usr/bin/bash
# CHANGELOG
# 2017-09-18 v2.1   prend arg
# 2017-09-03 v2.0   Version pour les 0 byte files aussi
# 2017-09-01 v1.2   Ajout defilement nom de dir
if [ -z $1 ]; 
then 
	dir="."; 
else 
	dir="$1";	
fi

echo Deleting $(find "$dir" -empty |wc -l) elements
find "$dir" -empty -delete -exec echo {} \;
echo Done! && sleep 3
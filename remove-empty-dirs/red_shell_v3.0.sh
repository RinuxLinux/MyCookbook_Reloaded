#! /usr/bin/sh
# CHANGELOG
# 2019-12-03 v3.0   Réécriture
# 2017-09-18 v2.1   prend dirname, relatif et absolue, en arg
# 2017-09-03 v2.0   Version pour les 0 byte files aussi
# 2017-09-01 v1.2   Ajout defilement nom de dir

if [ -z $1 ]; 
then 
	dir="."; 
else 
	dir="$1";	
fi

if [[ -z $2 ]];
then
	max="1";
else
	max="$2";
fi

echo Deleting $(find "$dir" -maxdepth ${max} -type d -empty |wc -l) elements

find "${dir}" -maxdepth ${max} -type d -empty -delete -print

echo Done!
sleep 3

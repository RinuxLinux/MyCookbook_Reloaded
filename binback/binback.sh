#! /usr/bin/env bash
#NOM......binback
#EXT......
#MAJOR....4
#MINOR....2
#DESCR....binback
#USAGE....binback [ -d descr | -u usage | -v version ]

# DEPENDENCIES: zip

# CHANGELOG
# ---------
# 2019-02-12 v4.2   adding switch for option parsing; new design 
# 2018-07-14 v4.1   fix zip destination full path
# 2018-07-11 v4.0   Refonte globale


USAGE=$(head -9 $0 | grep "#USAGE")
DESCR=$(head -9 $0 | grep "#DESCR")
VERSION="\033[1m$(basename $0)\033[0m version $(head -6 $0 | grep '#MAJOR....' | sed 's/#MAJOR....//g' ).$(head -6 $0 | grep '#MINOR....' | sed 's/#MINOR....//g' )"

case "$1" in
	"-usage" | "--usage" | "-u" )
		echo "\033[1;91mNOUVELLE NOTATION EN TEST\033[0m"
		echo $USAGE && exit 1
		;;
	"-descr" | "--descr" | "-d" )
		echo "\033[1;91mNOUVELLE NOTATION EN TEST\033[0m"
		echo $DESCR && exit 1
		;;
	"-version" | "--version" | "-v" )
		echo "\033[1;91mNOUVELLE NOTATION EN TEST\033[0m"
		echo $VERSION && exit 1
		;;
esac


#
# VAR
#

NOW=$(date +"%Y%m%d_%H%M%S")
NOW2=$(date +"%Y-%m-%d @ %H:%M:%S")
HOST=$(hostname)

DIR_LOCAL_BIN=${HOME}/bin
DIR_DBX_HOSTBIN=${HOME}/Dropbox/SCRIPTS/BACKUPS/MyBin_${HOST}
DIR_DBX_LIBRARY=${HOME}/Dropbox/SCRIPTS/BACKUPS/Library

#
# GARDE FOU
#

#
# Si LOCAL BIN n'existe pas, on sort
#
if [ ! -d $DIR_LOCAL_BIN ]; then
	echo "Le repertoire $HOME/bin n'existe pas";
	echo "Bye.";
	exit 1;
fi


#
# BACKUP Standard (Nom + Ext)
# MASK = NOM + EXT
# ORIG = LOCAL BIN
# DEST = DBX BIN
#

VIDE=0;
# Step 1. Si DBX_HOSTBIN n'existe pas, alors on le cree
if [ ! -d $DIR_DBX_HOSTBIN ]; then
	echo -e "\033[1mLe repertoire DBX/MyBin_${HOST} est introuvable et va etre cree :\033[0m";
	mkdir -pv $DIR_DBX_HOSTBIN 2>/dev/null ;
	VIDE=1 ;
fi

# Step 2. Si DBX_HOSTBIN n'est pas vide alors on zip et on le vide
if [ $VIDE=0 ]; then
	echo -e "\033[1mLe contenu DBX/MyBin_${HOST} va etre zippe...\033[0m";
	zip -uv "${HOME}/Dropbox/SCRIPTS/BACKUPS/MyBin_${HOST}_archive.zip" $DIR_DBX_HOSTBIN/* && echo -e "\033[3mzip zippidy zip zip\033[0m"
	echo -e "\033[1mSuppression du contenu de DBX/MyBin_${HOST} :\033[0m"
	rm -v ${DIR_DBX_HOSTBIN}/* ;
fi

# Step 3. Copier contenu de LOCAL_BIN vers DBX_HOSTBIN
echo -e "\033[1mCopie de LOCAL_BIN vers DBX/MyBin_${HOST} :\033[0m" ;
cp -vu ${DIR_LOCAL_BIN}/* ${DIR_DBX_HOSTBIN} ;


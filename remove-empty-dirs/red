#! /usr/bin/bash

isNumber() {
	case $1 in
	    ''|*[!0-9]*) 
			# 1 = True / est un nombre
			echo 0 ;; 
	  	*) 
			echo 1 ;;
		esac
}


echo "Setting up ..."

dir='.'
max=1

if [[ -d "$1" ]]; then
	dir="$1"
 	if [[ $(isNumber "$2") -eq 1 ]]; then 
 		max="$2" 
 	fi 
fi

if [[ -d "$2" ]]; then
	dir="$2"
 	if [[ $(isNumber "$1") -eq 1 ]]; then 
 		max="$1" 
 	fi 
fi

echo "Dir   : " $dir
echo "Depth : " $max 
echo "Proceeding ..."

find "$dir" -maxdepth "$max" -type d -empty -delete -print

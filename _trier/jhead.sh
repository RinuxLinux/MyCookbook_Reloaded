#!/bin/sh
# Snippets pour renommage JP*G avec JHEAD
# Essais

## 1
for file in *.{jpg,jpeg}; do
	taille=$(identify -format "%[w]x%[h]" "$file")
	jhead -n"%Y-%m-%d_%H%M%S_$taille" "$file"
done


## 2
for file in *.jpg; do
	taille=$(identify -format "%wx%h" "$file")
	jhead -n"%Y-%m-%d_%H%M%S_$taille" "$file"
done


## 3
for file in *; do 
	N1=$(date -d `echo "$file" | cut -c5- | cut -c-8` +"%Y-%m-%d") 
 	&& N2=$(echo "$file" | cut -c14-) 
 	&& mv -vn "$file" "${N1}_${N2}"
done 1>log.txt


## 4
for file in *.jpg; do 
	mv -vn "$file" $(echo "$file" | cut -c-17)_`identify -format "%wx%h" "$file"`.jpg 
done 1>>log.txt


## 5
for file in *.jpg ; do 
	EXT=$(echo "$file" | cut -c21-) ;
	DAT=$(date -d `echo "$file" | cut -c5-12` +"%Y-%m-%d") ;
	NO2=$(echo "$file" | cut -c14-19) ;
	DIM=$(identify -format "%wx%h" "$file") ;
	echo mv -vn "$file" "${DAT}_${NO2}_${DIM}.${EXT}" ; 
done 1>log.txt
	

## 6
for file in *.jpg; do 
	EXT=$(echo "$file" | cut -c19-) ;
	DIM=$(identify -format "%wx%h" "$file") ;
	NO2=$(basename -s .jpg "$file") ;
	mv -nv "$file" "$NO2"_"$DIM"."$EXT" ; 
	done 1> log.txt


## 7
# Basename sans extension
# $ basename -s .jpg 2016-05-17_170730b.jpg 
# => 2016-05-17_170730b


## 8
# REGEX
dir0="/media/reno/61EC-BDC0/DCIM/102_PANA" ;
dir1="/home/reno/Dropbox/Camera Uploads/JAN/AREN" ;

# chercher les erreurs du type 2 x les dimensions
for file in */*; do 
	echo `basename "$file"` | egrep "^[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{6}(_[0-9]+x[0-9]+){2,}.jpg$"; 
done 

# plus simple
for file in */*; do 
	echo `basename "$file"` | egrep "^[0-9]{4}-[0-9-_]+(_[0-9]+x[0-9]+){2,}.[jpgJPG]$"; 
done 


# RESET
for file in *.jpg; do 
	jhead -n"%Y-%m-%d_%H%M%S" "$file" 
done




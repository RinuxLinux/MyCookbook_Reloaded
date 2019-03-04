#! /usr/bin/bash
# Sauvegarder les nfo du rep TV-F2
# v1.0 2017-10-10

if [ -f "nfos.tar" ]; then
	echo "--> Updating existing archive..."
	tar uvf nfos.tar *.nfo
	tar uvf nfos.tar *.jpg 2>/dev/null
else
	echo "--> Creating archive..."
	tar cvf nfos.tar *.nfo *.jpg
fi


for f in *.nfo; 
do
	trigger="False"
	fname="${f%.nfo}"
	
	if [ -f "$fname.avi" ]; then
		trigger="True"
	fi
	
	if [ -f "$fname.mkv" ]; then
		trigger="True"
	fi
	
	if [ -f "$fname.mp4" ]; then
		trigger="True"
	fi
	
	if [ -f "$fname.ts" ]; then
		trigger="True"
	fi
	
	if [ $trigger == "False" ]; then
		rm -v $f
	fi
done
	
echo "--> Sauvegarde des *.nfo dans $PWD terminée"
sleep 2s
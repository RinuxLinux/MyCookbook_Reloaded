#/bin/sh
# Creer un dossier et y mettre les fichiers 
# v1.1

NOW=$(date +"%F")

replace_space_with_dash() {
	ret=${*//\'/-}
	ret=${ret//\ /-}
	ret=${ret//--/-}
	echo "$ret"
}

proper() {
	# Ceci Est Un Exemple
	ret=''
	for el in ${*//\'/\ }; do
		el=${el,,};
		el=${el^};
		ret+="$el "
	done
	echo $ret
}

upper() {
	# CECI EST UN EXEMPLE
	echo ${*^^}
}

capitalize() {
	# Ceci est un exemple
	ret=${*,,}
	ret=${ret^}
	echo $ret
}

main() {
	#echo "ENTREPRISE ? "
	read -p "DATE       ? " da
	read -p "ENTREPRISE ? " cie
	read -p "Ville      ? " ville
	read -p "Job        ? " job

	if [ -z "$da" ]; then
		da=${NOW};
	fi

	cie=$(upper "$cie")
	cie=$(replace_space_with_dash "$cie")
	
	ville=$(proper "$ville")
	ville=$(replace_space_with_dash "$ville")
	
	job=$(proper "$job")
	job=$(replace_space_with_dash "$job")

	newdir="${da}_${cie}-${ville}_${job}"

	echo "-----------"
	echo "Entr.: " $cie
	echo "Ville: " $ville
	echo "Poste: " $job
	echo -e "Newdir: \033[1;32m$newdir\033[0m"
	read -p "Confirmer ? Y/n " ans

	case $ans in
		["yY"])
			DIR=$newdir

			mkdir -v "$DIR" 2>/dev/null && touch "$DIR/notes.txt" "$DIR/annonce.txt" "$DIR/lm.txt"
			
			read -p "Ouvrir ? Y/n " ans2
			case "$ans2" in
				["yY"]) 
					explorer "$DIR" ;;
				*) 
					echo "ok bye." ;;
			esac
			;;
		*)
			echo -e "\033[1;31mAnnulé\033[0m"
			;;
	esac
}


ans3="Y"
while [ "$ans3" == "Y" ] || [ "$ans3" == "y" ]; do
	main
	echo -e "\033[1;32m---------------\033[0m"
	read -p "Un autre ? Y/n " ans3
	echo -e "\033[1;32m---------------\033[0m"
done

echo "ok bye." 
exit
#/bin/sh
# Creer un dossier et y mettre les fichiers 
# v1.3


#########################
### G L O B A L E S   ###
#########################

NOW=$(date +"%F")
DIR_LM='/z/Dropbox/LABO-DBX/cv-lm/lms'
DIR_CV='/z/Dropbox/LABO-DBX/cv-lm/_latest'

### Colors in terminal
bold="\033[1m"
normal="\033[0m"

bg_black="\033[40m"
bg_red="\033[41m"
bg_green="\033[42m"
bg_yellow="\033[43m"
bg_blue="\033[44m"
bg_magenta="\033[45m"
bg_cyan="\033[46m"
bg_white="\033[47m"

fg_black="\033[30;1m"
fg_red="\033[31;1m"
fg_green="\033[32;1m"
fg_yellow="\033[33;1m"
fg_blue="\033[34;1m"
fg_magenta="\033[35;1m"
fg_cyan="\033[36;1m"
fg_white="\033[37;1m"
fg_fat_red="\033[1;31m"

#########################
### F O N C T I O N S ###
#########################

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


lower() {
	# ceci est un test
	echo "${*,,}"
}


get_file() {
	# Copie de fichier venant de $DIR_CV
	# $1 = nom fichier (ex: 'cv-alt.pdf')
	# $2 = destination (ex: "$DIR")
	if [ -f "$DIR_CV/$1" ]; then
		cp -vn "$DIR_CV/$1" "$2"
	else
		echo -e "${fg_red}ERREUR ... Le fichier $1 n'existe pas ${normal}"
	fi
}


select_cv() {
	# USAGE
	# select_cv "$DIR"
	DEST=$1
	
	echo -ne "${fg_cyan}${bg_black}"
	echo "Choisir un cv:"
	echo "1) cv-alt"
	echo "2) cv-dev neutre"
	echo "3) cv-ged"
	echo "4) cv-xp"
	echo "5) Aucun"
	read -p "Choix: " choix
	echo -ne "${normal}"

	case $choix in
		1) 	get_file "cv_alt.pdf" "$DEST"
			;;
		2) 	get_file "cv_dev_n.pdf" "$DEST"
			;;
		3) 	get_file "cv_ged.pdf" "$DEST"
			;;
		4) 	get_file "cv_xp.pdf" "$DEST"
			;;
		5)  ;;
		["dD"])
			echo -e "${fg_magenta}Debug select_cv ${normal}"
			;; 
		*) 	echo -e "${fg_red}Choix non disponible. ${normal}"
			;;
	esac

}


select_date() {
	# USAGE
	# date=$(select_date)
	read -p "DATE       ? " da
	
	if [ -z "$da" ]; then
		da=${NOW};
	fi

	echo "$da"
}


select_cie() {
	# USAGE
	# cie="$(select_cie)"
	read -p "ENTREPRISE ? " cie

	cie=$(upper "$cie")
	cie=$(replace_space_with_dash "$cie")

	echo "$cie"
}


select_ville() {
	# USAGE
	# ville="$(select_ville)"
	read -p "Ville      ? " ville

	ville=$(proper "$ville")
	ville=$(replace_space_with_dash "$ville")

	echo "$ville"
}


select_job() {
	# USAGE
	# job="$(select_job)"
	read -p "Job        ? " job

	job=$(proper "$job")
	job=$(replace_space_with_dash "$job")

	echo "$job"
}


setup_dir(){
	# USAGE
	# setup_dir "$newdir"
	ndir="$1"

 	echo -e "${fg_green}${bg_black}Setting up dir ...${normal}"
	mkdir -p "$ndir" 2>/dev/null && touch "$ndir/notes.txt" "$ndir/annonce.txt" "$ndir/lm.txt" || echo -e "${fg_fat_red}ECHEC mkdir $ndir ${normal}" 		
}


import_template() {
	# USAGE
	# import_template "$newdir"
	ndir="$1"

	echo -en "${fg_cyan}${bg_black}Importer 'mail_type.txt' ? [Y] ${normal}"
	read template
		
	case "$template" in 
		["yY"]) 
			get_file "mail_type.txt" "$ndir"
			;;
		["dD"])
			echo -e "${fg_magenta}Debug import_template ${normal}"
			;; 
	esac 
}


import_lm_docx() {
	# USAGE
	# import_lm_docx "$cie"
	dest="$1"
	cie="$2"

	echo -en "${fg_green}${bg_black}Importer 'lm_${cie,,}.docx' ? [Y] ${normal}"
	read lm
		
	case "$lm" in 
		["yY"]) 
			cp -v "$DIR_LM/lm.docx" "$dest/lm_${cie,,}.docx"
			;;
		["dD"])
			echo -e "${fg_magenta}Debug import_lm_docx ${normal}"
			;; 
	esac 
}


import_tools() {
	# USAGE
	# import_tools "$newdir"
	ndir="$1"
	
	echo -en "${fg_cyan}${bg_black}Si BDM JOBS, importer parsing tools ? [Y] ${normal}"
	read importer
			
	case "$importer" in 
		["yY"]) 
			get_file "parsehtml.py" "$ndir"
			touch "$ndir/parseme.txt"
			;;
		["dD"])
			echo -e "${fg_magenta}Debug import_tools ${normal}"
			;; 
	esac 
}


open_notes_in_vim() {
	# USAGE
	# import_tools "$newdir"
	ndir="$1"

	echo -en "${fg_green}${bg_black}Ouvrir 'notes.txt' avec Vim [V] ? [Y|V] ${normal}"
	read ans2

	case "$ans2" in
		["yYvV"]) 
			vim "$ndir/notes.txt"
			;;
		["dD"])
			echo -e "${fg_magenta}Debug open_notes_in_vim ${normal}"
			;; 
	esac
}

write_reponse_in_vim() {
	ndir="$1"
	echo -en "${fg_cyan}${bg_black}Ecrire 'reponse.txt' via Vim ? [Y] ${normal}"	
	read reponse

	case "$reponse" in
		["Yy"])
			vim "${ndir}/reponse.txt"
			;;
		["dD"])
			echo -e "${fg_magenta}Debug write_reponse_in_vim ${normal}"
			;; 
	esac
}


open_dir_in_explorer() {
	# USAGE
	# open_dir_in_explorer "$newdir"
	ndir="$1"
				
	echo -en "${fg_green}${bg_black}Ouvrir dir ? [Y|O] ${normal}"				
	read ans4
				
	case "$ans4" in
		["yY"]) 
			explorer "$ndir" 
			;;
		["oO"])
			explorer "$ndir"
			sortie
			;;
			
		["dD"])
			echo -e "${fg_magenta}Debug open_dir_in_explorer${normal}"
			;; 
		*) 
			echo -e "${fg_fat_red}ok bye.${normal}"
			;;
	esac
}


write_reponse_in_vim() {
	ndir="$1"
	echo -en "${fg_cyan}${bg_black}Ecrire 'reponse.txt' via Vim ? [Y] ${normal}"	
	read reponse

	case "$reponse" in
		["Yy"])
			vim "${ndir}/reponse.txt"
			;;
		["dD"])
			echo -e "${fg_magenta}Debug write_reponse_in_vim ${normal}"
			;; 
	esac
}

sortie() {
	echo -e "${bg_yellow}${fg_white}ok bye.${normal}" 
	exit
}


main() {
	da="$(select_date)"
	cie="$(select_cie)"
	ville="$(select_ville)"
	job="$(select_job)"

	job=$(echo "${job//Cs-Via-Sw/CS-via-SW}")
	job=$(echo "${job//-It/-IT}")

	newdir="${da}_${cie}_${ville}_${job}"

	echo "-----------"
	echo "Entr.: " $cie
	echo "Ville: " $ville
	echo "Poste: " $job
	echo -e "Newdir: \033[1;32m$newdir\033[0m"
	echo "-----------"
	echo -en "${fg_green}Confirmer ? [Y] ${normal}"
	read confirm

	case $confirm in
		["yY"])
			echo -e "${fg_magenta}Note: A partir d'ici, entrer 'd' pour DEBUG   ${normal}"
			echo -e "${fg_magenta}      mais le dir sera quand même créé.       ${normal}"
			setup_dir "$newdir"
			select_cv "$newdir"
			import_template "$newdir"
			import_lm_docx "$newdir" "$cie" 
			import_tools "$newdir"
			open_notes_in_vim "$newdir"
			write_reponse_in_vim "$newdir"
			open_dir_in_explorer "$newdir"
			;;
		*)
			echo -e "\033[1;31mAnnulé\033[0m"
			;;
	esac

	echo -ne "${normal}"
}

#################################################

ans3="Y"
while [ "$ans3" == "Y" ] || [ "$ans3" == "y" ]; do
	main
	echo -e  "${fg_green}---------------${normal}"
	echo -en "${fg_green}Un autre ? [Y] ${normal}" 
	read ans3
	echo -e  "${fg_green}---------------${normal}"
done

sortie
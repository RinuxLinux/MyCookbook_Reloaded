#!/bin/sh
# set up dossier candidature


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


check_date() {
	# check if date is not empty
	# if empty, returns now; else returns date
	da="$1"
	if [ -z "$da" ]; then
		da=${NOW};
	fi

	echo "$da"
}


check_cie() {
	# put $cie in correct case
	cie=$(upper "$1")
	cie=$(replace_space_with_dash "$cie")

	echo "$cie"
}


check_ville() {
	# put $ville in correct case
	ville=$(proper "$1")
	ville=$(replace_space_with_dash "$ville")

	echo "$ville"
}


check_job() {
	# put $job in correct case
	job=$(proper "$1")
	job=$(replace_space_with_dash "$job")
	job=$(echo "${job//Cs-Via-Sw/CS-via-SW}")
	job=$(echo "${job//-It/-IT}")
	
	echo "$job"
}


#########################
### M A I N           ###
#########################

main2() {
	count=0;
	while [ $count == 0 ]; do
		read -p "DATE  ? " da
		read -p "CIE   ? " cie 
		read -p "VILLE ? " ville 
		read -p "JOB   ? " job

		da=$(check_date "$da")
		cie=$(check_cie "$cie")
		ville=$(check_ville "$ville")
		job=$(check_job "$job")

		newdir="${da}_${cie}_${ville}_${job}"

		echo "-----------"
		echo "Entr.: " $cie
		echo "Ville: " $ville
		echo "Poste: " $job
		echo -e "Newdir: \033[1;32m$newdir\033[0m"
		echo "-----------"
		echo -en "${fg_green}[C]onfirmer ? [R]ecommencer ? [Q]uitter ? ${normal}"
		read confirm

		case $confirm in
			["YyCc"])
				#echo "Confirmed, quit the loop"
				count=1
				;;
			["Qq"])
				#echo "Cancel and quit"
				count=2
				;;
			*)
				#echo "Cancel and repeat"
				;;
		esac
	done

	case $count in 
		1)
			echo "Processing with $newdir."
			;;
		2)
			echo "Closing. Bye !"
			exit
			;;
		esac

	echo "SELECTING PROCESS"
	echo "1- par [C]V"
	echo "2- par [P]ROFIL"
	echo "q- [Q]uitter"
	read choix_180

	case $choix_180 in
#		1)	echo "PAR CV" ;;
		["1cC"]) echo "PAR CV" ;;
		["2pP"]) echo "PAR Profil" ;;
#		2)  echo "PAR PROFIL";;
		*) 
			echo "Création de $newdir annulée"
			echo "[R]ecommencer ? [Q]uitter ?"
			read choix_188
			case $choix_188 in
				["rR"]) echo "Recommencons" ;;
				*) echo "Quittons" ;;
			esac
			;;
	esac


}


select_cv() {
	# USAGE
	# select_cv "$DIR"
	DEST=$1
	
	echo -ne "${fg_cyan}${bg_black}"
	echo "+---------------+"
	echo "| IMPORT PAR CV |"
	echo "+---------------+"
	echo "1) cv-alt"
	echo "2) cv-dev neutre"
	echo "3) cv-ged"
	echo "4) cv-xp"
	echo "5) Aucun"
	read -p "Choisir un cv: " cv
	echo -ne "${normal}"

	case $choix in
		1) 	# get_file "cv_alt.pdf" "$DEST"
			echo "get cv-alt"
			;;
		2) 	# get_file "cv_dev_n.pdf" "$DEST"
			echo "get cv-dev"
			;;
		3) 	# get_file "cv_ged.pdf" "$DEST"
			echo "get cv-ged"
			;;
		4) 	# get_file "cv_xp.pdf" "$DEST"
			echo "get cv-xp"
			;;
		5)  ;;
		["dD"])
			echo -e "${fg_magenta}Debug select_cv ${normal}"
			;; 
		*) 	echo -e "${fg_red}Choix non disponible. ${normal}"
			;;
	esac
}

select_profil() {
	# USAGE
	# select_profil "$newdir" "$cie"
	DEST=$1
	cie=$2

	echo "+-------------------+"
	echo "| IMPORT PAR PROFIL |"
	echo "+-------------------+"
	echo "1) dev alt leg - Legit ad"
	echo "2) dev alt hij - Hijacking another ad"
	echo "3) dev alt cs  - CS"
	echo "4) op saisie"
	echo "5) op numerisation"
	echo "6) Aucun / Annuler"
	read -p "Choisir un profil: " profil

	case $profil in
		1) 	# dev alt legit
			;&

		2) 	# dev alt hijack
			;&

		3) 	# dev alt CS
			# get_file "cv_alt.pdf" "$DEST"
			# cp -v "$DIR_LM/lm.docx" "$dest/lm_${cie,,}.docx"
			# get_file "mail_type.txt" "$dest"
			echo "copy cv-alt"
			echo "get short_lm.txt"
			echo "get lm_$cie.docx"
			;;

		4)  # op saisie (cv_xp)
			echo "copy cv-xp ou cv_ged"
			echo "get short lm speciale op saisie"
			echo "get lm.docx special op saisie"
			echo "En resumé, get everything from special folder"
			;;

		5)	# op numerisation (cv_ged)
			echo "copy cv_ged"
			echo "get short lm speciale op num"
			echo "get lm.docx special op num"
			echo "En resumé, get everything from special folder"
			;;

		["dD"])
			echo "Debug select_profil"
			;; 
		*) 	echo "Choix non disponible."
			;;
	esac
}


select_lm () {
	# importer ou non lm template
	dest="$1"
	cie="$2"

	echo "+-------------------+"
	echo "| IMPORT LM         |"
	echo "+-------------------+"
	echo "1) Importer juste mail_type.txt (collection de lm courtes)"
	echo "2) Importer juste 'lm_${cie,,}.docx'"
	echo "3) Importer les deux"
	read lm

	if [ $lm == 1 ]; then
		# get_file "mail_type.txt" "$dest"
		echo "txt"
	elif [ $lm == 2 ]; then 
		# cp -v "$DIR_LM/lm.docx" "$dest/lm_${cie,,}.docx"
		echo "doc"
	elif [ $lm == 3 ]; then
		# get_file "mail_type.txt" "$dest"
		# cp -v "$DIR_LM/lm.docx" "$dest/lm_${cie,,}.docx"
		echo "les deux"
	else
		echo "Aucun, ANNULATION"
	fi
}



main() {
	count=0;
	cv=0
	profil=0
	parsing=0

	while [ $count == 0 ]; do
		read -p "DATE  ? " da
		read -p "CIE   ? " cie 
		read -p "VILLE ? " ville 
		read -p "JOB   ? " job

		da=$(check_date "$da")
		cie=$(check_cie "$cie")
		ville=$(check_ville "$ville")
		job=$(check_job "$job")

		newdir="${da}_${cie}_${ville}_${job}"

		echo "-----------"
		echo "Entr.: " $cie
		echo "Ville: " $ville
		echo "Poste: " $job
		echo -e "Newdir: \033[1;32m$newdir\033[0m"
		echo "-----------"
		echo -en "${fg_green}[C]onfirmer ? [R]ecommencer ? [Q]uitter ? ${normal}"
		read confirm

		case $confirm in 
			["YyCc"])
				echo "Importer par [C]V ou par [P]rofil ? [A]nnuler"
				read choix_228
				case "$choix_228" in
					["Cc1"])
						select_cv "$newdir"
						select_lm "$newdir" "$cie"
						;;
					["Pp2"])
						select_profil "$newdir" "$cie"
						;;
					*) 	echo "Annulation"
						exit
						;;
				esac

				echo "Importer outil pour parser offre BDM-JOBS ? [Y] "
				read choix_280
				case "$choix_280" in
					["YyOo"])
						# cp 
						;;
				esac

				echo "creation rep"
				echo "import des docs"

				echo "Un autre ?"
				echo "si non: count=1"
				;;
			["Qq"])
				echo "Quit"
				exit;;
			*)
				;;
		esac
	done


}

main
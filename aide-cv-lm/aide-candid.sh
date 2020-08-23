#!/usr/bin/sh
# Aide pour poser candidature CV / LM

select_profil() {
	# USAGE
	# select_cv "$DIR"
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
		#cp -v "$DIR_LM/lm.docx" "$dest/lm_${cie,,}.docx"
		echo "doc"
	elif [ $lm == 3 ]; then
		echo "les deux"
	else
		echo "Aucun, ANNULATION"
	fi
}
select_profil here cie

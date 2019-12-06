#! /bin/sh
# Backup HTDOCS SELF

echo "Archivage sélectif et horodaté de htdocs."
echo "-----------------------------------------"


if [[ -d /p/ ]]; then 
	
	$host='self'
	#today=$(date +"%F")
	today=$(date +"%Y-%m-%d_%H%M%S")
	ignore_list=(dashboard img triage webalizer wampp xampp)
	
	src="/c/xampp/htdocs"
	take_list=()
	no_list=()

	for i in ${ignore_list[@]}; do
		no_list+=("${src}/${i}")
	done


	for d in $src/*; do
		if [[ -d $d ]]; then
			take_list+=("$d")
		fi
	done	


	for i in ${no_list[@]}; do
		delete=("$i")
		for target in "${delete[@]}"; do
			for i in "${!take_list[@]}"; do
				if [[ ${take_list[i]} = $target ]]; then
					unset 'take_list[i]'
				fi
			done
		done
	done


	for f in ${take_list[@]}; do
		tar uvf /p/bk_${host}_htdocs_${today}.tar "$f"
	done


	echo '---------- FIN --------------'
	echo "Archive : bk_${host}_htdocs_${today}.tar"
	for f in ${take_list[@]}; do
		echo "$f"
	done
	echo '---------- FIN --------------'

else
	echo "Répertoire P:/ introuvable. Lancez pCloud."
fi

sleep 3


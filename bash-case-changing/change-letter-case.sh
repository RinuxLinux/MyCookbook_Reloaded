#/bin/sh
# Changer la casse d'un mot ou d'une phrase 
# 2019-03-25 v1.0


proper() {
	# Ceci Est Un Exemple
	ret=''
	for el in ${*//\'/\ }; do
		el=${el,,}
		el=${el^}
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
	# ceci est un exemple
	ret=''
	for el in ${*//\'/\ }; do
		ret+="${el,,} "
	done
	echo $ret
}



# USAGE:
upp=$(upper "cEcI est UN Test")
cap=$(capitalize "cEcI est UN Test")
low=$(lower "cEcI est UN Test")
pro=$(proper "cEcI est UN Test")



for f in *.pdf
do 
	echo "$(basename $f);"$(pdftk "$f" dump_data|grep NumberOfPages) >> output.csv
done
sed -i 's/NumberOfPages:\ //g' output.csv

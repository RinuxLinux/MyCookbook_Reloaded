#!/usr/bin/bash
# CHANGELOG
# 2017-09-01 v1.2   Ajout defilement nom de dir

echo Deleting $(find . -type d -empty |wc -l) folders
find . -type d -empty -delete -exec echo {} \;
echo Done! && sleep 5
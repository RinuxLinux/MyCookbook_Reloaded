#!/bin/sh
echo "Deleting EMPTY FILES..."
find . -type f -empty -delete -print
rm -v */mail_type.txt 2>/dev/null
echo '-----------------------'
echo "Deleting EMPTY DIR..."
find . -type d -empty -delete -print
echo "done CLEANING."

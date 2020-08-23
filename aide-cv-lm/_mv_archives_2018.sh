#!/bin/sh
mkdir -v "_2018" "_2019_Q1" "_2019_Q2" 2>/dev/null
for d in 2018-*; do 
	[ -d "$d" ] && mv -v "$d" _2018/
done

for d in 2019-{01,02,03}*; do 
	[ -d "$d" ] && mv -v "$d" _2019_Q1/
done

:'
for d in 2019-{04,05,06}*; do 
	[ -d "$d" ] && mv -v "$d" _2019_Q2/
done

'
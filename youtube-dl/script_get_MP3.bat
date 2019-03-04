@ECHO OFF
set _my_datetime=%date%_%time%
set _my_datetime=%_my_datetime: =_%
set _my_datetime=%_my_datetime::=%
set _my_datetime=%_my_datetime:/=_%
set _my_datetime=%_my_datetime:.=_%

cd "F:\DL\Mouh-x\youtube-dl"

REM   youtube-dl mp3 only
REM   youtube-dl --audio-quality 0 --audio-format "mp3" -x https://www.youtube.com/watch?v=LFoQe8bL6UU
REM   -x 	extract audio
REM   -a 	input is a file with URLs
REM   https://www.youtube.com/watch?v= 

REM FROM LIST
youtube-dl --audio-quality 0 --audio-format "mp3" -x -a "liens-mp3.lst"

echo ---------------------------- >> "liens-mp3.lst"
echo Fait %_my_datetime% >> "liens-mp3.lst"
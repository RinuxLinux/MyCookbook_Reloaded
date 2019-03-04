@ECHO OFF
SETLOCAL
set _my_datetime=%date%_%time%
set _my_datetime=%_my_datetime: =_%
set _my_datetime=%_my_datetime::=%
set _my_datetime=%_my_datetime:/=_%
set _my_datetime=%_my_datetime:.=_%

cd "F:\DL\Mouh-x\youtube-dl"

youtube-dl -f 137+140 -a liens.lst  || youtube-dl -f 136+140 -a liens.lst || youtube-dl -f best -a liens.lst >> "log_%_my_datetime%.log" 2>&1
rem youtube-dl -f best -a liens.lst
echo   >> liens.lst
echo Fait %_my_datetime% >> liens.lst

REM GET FORMATS
rem youtube-dl -F -a liens.lst > liens-formats.list

rem youtube-dl -f "mp4" http://www.canalplus.fr/c-emissions/pid1830-c-zapping.html?vid=1404126

REM KASSOS : youtube-dl -f 137+140 https://www.youtube.com/watch?v=FD3i31DGAMI
REM ARTE   : youtube-dl -F http://future.arte.tv/fr/tu-mourras-moins-bete-la-serie/c-est-quoi-une-near-death-experience-tu-mourras-moins-bete-1930
REM IMDB   : youtube-dl -f "1080p" "URL"
REM CANAL  : youtube-dl -f "HD" http://www.canalplus.fr/redirect_pfv.php?vid=1397458

REM youtube-dl -f 137+140 https://www.youtube.com/watch?v=wBZtM8q2Z1g


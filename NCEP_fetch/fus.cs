cd /Users/WRF4.1/NCEP
if [ -e auth.rda.ucar.edu ];then rm -f auth.rda.ucar.edu;fi
./ff.py
./uu.py
./ss.py
n=$(grep done crontab_log.txt|wc -l)
if ! [ $n == 12 ];then 
d=$(date "+%Y/%m/%d")
/usr/bin/osascript -e 'tell app "System Events" to display dialog "Something wrong in fus.cs @'$d' !"' &
fi

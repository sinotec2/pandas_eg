echo $(( $(wc -l $1|/opt/local/bin/awkk 1) - 1 )) > $1.bln
sed 1d $1 >> $1.bln

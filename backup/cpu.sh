grep 'cpu' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print "CPU " usage "%"}'
free | grep Mem | awk '{print "Mem "  $3/$2*100.0 "%"}'

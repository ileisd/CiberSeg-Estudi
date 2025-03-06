#!/usr/bin/bash

########################################################
# Fet per ileisd com a preparació de la prova del eJPT #
########################################################

while getopts "u:w:f" flag; do
  case $flag in
    u) # URL
    url=$OPTARG
    ;;
    w) # Dirlist
    dirlist=$OPTARG
  esac
done

tput civis
touch test.txt

while read -r dir; do
  put=$(curl -L -s -o /dev/null -w "%{http_code}" "$url/$dir" --upload-file test.txt 2>&1)
  if [ "$put" != "405" ]; then
    echo "[+] $url/$dir allows PUT request"
  fi
done < $dirlist

rm test.txt
tput cnorm

!/usr/bin/bash

#                                                      #
# Fet per ileisd com a preparació de la prova del eJPT #
#                                                      #

while getopts "H:w:u:p:" flag; do
  case $flag in
    H) # Host
    host=$OPTARG
    ;;
    w) # Wordlist
    wordlist=$OPTARG
    ;;
    u) # User
    user=$OPTARG
    ;;
    p) # Password
    pass=$OPTARG
    ;;
    \?) # Invalid
    echo "[*] Usage: smbsharenum -H [host] -w [wordlist]"
    exit 1
    ;;
  esac
done

tput civis

echo " "
if [ ! -z "$user" ]; then
  while read -r LINE
  do
    if smbclient -U $user%$pass \\\\$host\\$LINE > /dev/null; then
      echo "[+] $LINE is a valid share for user $user"
    fi
  done < $wordlist
else
  while read -r LINE
  do
    if smbclient -U '' -N \\\\$host\\$LINE > /dev/null; then
      echo "[+] $LINE is a valid share in a NULL Session"
    fi
  done < $wordlist
fi

tput cnorm

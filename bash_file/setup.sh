#!/bin/bash
blue="\e[34m"
default="\e[0m"
green="\033[92m"
red="\e[1;31m"
yellow="\e[0;33m"

clear
echo -e "$blue   ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗ "
echo -e "$blue  ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝ "
echo -e "$blue  ██║     ███████║█████╗  ██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗"
echo -e "$blue  ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║"
echo -e "$blue  ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝██╗██╗██╗"
echo -e "$blue   ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝╚═╝"
echo -e "$blue\n -------------------------- Giovanni Iannaccone --------------------------"

echo -e "\n"
sleep 1

#checking for root user
echo -e "$yellow [ * ] Checking for root user"
echo -e "$default [User: $USER]"
if [[ $EUID -ne 0 ]]; then
   echo -ne "$red [ x ]::[User]: ( no root )"
   sleep 0.5
   exit 1
else
    echo -e "$green [ ✔ ]::[User]: ROOT"
    sleep 0.5
fi

#checking for internet connection
echo -e "$yellow [ * ] Checking for internet connection"
echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1
if [ "$?" -ne "0" ]; then
    echo -e "$red [ X ]::[Internet Connection]: OFFLINE!"
    sleep 0.5
    exit 1
else
    echo -e "$green [ ✔ ]::[Internet Connection]: ONLINE"
    sleep 0.5
fi

echo -e "\n$blue [-- Starting $ IANS $ --]"
sleep 1

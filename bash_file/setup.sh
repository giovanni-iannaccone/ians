#!/bin/bash
blue="\e[34m"
default="\e[0;0m"
green="\033[92m"
red="\e[1;31m"
yellow="\e[0;33m"

clear
echo -e
echo -e "$blue   ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗ $default"
echo -e "$blue  ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝ $default"
echo -e "$blue  ██║     ███████║█████╗  ██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗ $default"
echo -e "$blue  ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║ $default"
echo -e "$blue  ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝██╗██╗██╗ $default"
echo -e "$blue   ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝╚═╝ $default"
echo -e
echo -e "$blue -------------------------- Giovanni Iannaccone -------------------------- $default"

echo -e
sleep 1

#checking for root user
echo -e "$yellow [ * ] Checking for root user $default"
echo -e "$default [User: $USER]"
if [[ $EUID -ne 0 ]]; then
   echo -ne "$red [ x ]::[User]: ( no root ) $default"
   sleep 0.5
   echo -e "$default"
   exit 1
else
    echo -e "$green [ ✔ ]::[User]: ROOT $default"
    sleep 0.5
fi

#checking for internet connection
echo -e "$yellow [ * ] Checking for internet connection $default"
if ping -q -c 1 -W 1 8.8.8.8 > /dev/null;
then
    echo -e "$green [ X ]::[Internet Connection]: ONLINE $default"
    sleep 0.5
else
    echo -e "$red [ ✔ ]::[Internet Connection]: OFFLINE $default"
    sleep 0.5
    echo -e "$default"
    exit 1
fi

echo -e "\n$blue [-- Starting $ IANS $ --] $default"
sleep 1

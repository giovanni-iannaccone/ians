blue="\e[34m"
default="\e[0;0m"
green="\033[92m"
red="\e[1;31m"
yellow="\e[0;33m"

clear
echo -e
echo -e "$blue ██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗     ██╗███╗   ██╗ ██████╗           $default"
echo -e "$blue ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║     ██║████╗  ██║██╔════╝           $default"
echo -e "$blue ██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║     ██║██╔██╗ ██║██║  ███╗          $default"
echo -e "$blue ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║     ██║██║╚██╗██║██║   ██║          $default"
echo -e "$blue ██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗██║██║ ╚████║╚██████╔╝██╗██╗██╗ $default"
echo -e "$blue ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝╚═╝ $default"

echo -e

#checking for internet connection
echo -e "$yellow [ * ] Checking for internet connection $default"
if ping -q -c 1 -W 1 8.8.8.8 > /dev/null;
then
    echo -e "$green [ X ]::[Internet Connection]: ONLINE $default"
    sleep 0.5
else
    echo -e "$red [ ✔ ]::[Internet Connection]: OFFLINE $default"
    sleep 0.5
    exit 1
fi

#checking for golang
echo -e "$yellow [ * ] Checking for golang $default"
which go > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
    echo -e "$green [ ✔ ]::[Go]: found $default"
    sleep 1
else
    echo -e "$red [ X ]::[Go]: go not found $default"
    sleep 1
    echo -e "$yellow [!]::[Installing golang...] $default"
    apt install golang-go || pacman -S go
fi

#install crypto/ssh
cd internal/bruteforce
go get https://golang.org/x/crypto/ssh
cd ../..

#checking for python
echo -e "$yellow [ * ] Checking for python $default"
which python > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
    echo -e "$green [ ✔ ]::[Python]: found $default"
    sleep 1
else
    echo -e "$red [ X ]::[Python]: python not found $default"
    sleep 1
    echo -e "$yellow [!]::[Installing Module Python...] $default"
    apt install python3 || pacman -S python3
    apt install pip || pacman -S pip
    apt install pip2 || pacman -S pip2
    pip2 install --upgrade pip
fi

echo -e "$blue Done, press ENTER to continue $default"
read

exit 0
fi
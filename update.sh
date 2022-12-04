blue="\e[34m"

clear
echo -e
echo -e "$blue  ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗██╗███╗   ██╗ ██████╗           $default"
echo -e "$blue  ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║████╗  ██║██╔════╝           $default"
echo -e "$blue  ██║   ██║██████╔╝██║  ██║███████║   ██║   ██║██╔██╗ ██║██║  ███╗          $default"
echo -e "$blue  ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██║██║╚██╗██║██║   ██║          $default"
echo -e "$blue  ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ██║██║ ╚████║╚██████╔╝██╗██╗██╗ $default"
echo -e "$blue   ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝╚═╝ $default"
echo -e

#checking for internet connection
echo -e "$yellow [ * ] Checking for internet connection $default"
if ping -q -c 1 -W 1 8.8.8.8 > /dev/null;
then
    echo -e "$green [ ✔ ]::[Internet Connection]: ONLINE $default"
    sleep 0.5
else
    echo -e "$red [ X ]::[Internet Connection]: OFFLINE $default"
    sleep 0.5
    exit 1
fi

#checking for git
echo -e "$yellow [ * ] Checking for git $default"
if git > /dev/null;
then
    echo -e "$green [ ✔ ]::[git]: found $default"
    sleep 0.5
else
    echo -e "$red [ X ]::[git] not found $default"
    apt install git || pacman -S install git

chmod +x /etc/
chmod +x /usr/share/doc
cd ..
rm -rf ians
git clone https://github.com/giovanni-iannaccone/ians
chmod +x install.sh
echo -e "$blue Installing the newest version"
./install.sh
clear

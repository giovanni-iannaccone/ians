blue="\e[34m"

clear
echo  -e "$blue  ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗██╗███╗   ██╗ ██████╗          "
echo  -e "$blue  ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║████╗  ██║██╔════╝         "
echo  -e "$blue  ██║   ██║██████╔╝██║  ██║███████║   ██║   ██║██╔██╗ ██║██║  ███╗         "
echo  -e "$blue  ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██║██║╚██╗██║██║   ██║         "
echo  -e "$blue  ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ██║██║ ╚████║╚██████╔╝██╗██╗██╗"
echo  -e "$blue   ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝╚═╝"

#checking for internet connection
echo -e "$yellow [ * ] Checking for internet connection"
if ping -q -c -l -W 1 8.8.8.1 > /dev/null;
then
    echo -e "$green [ X ]::[Internet Connection]: ONLINE"
    sleep 0.5
else
    echo -e "$red [ ✔ ]::[Internet Connection]: OFFLINE"
    sleep 0.5
    echo -e "$default"
    exit 1
fi

chmod +x /etc/
chmod +x /usr/share/doc
cd ..
cd ..
rm -rf ians
git clone https://github.com/giovanni-iannaccone/ians
chmod +x bash_file/install.sh
echo -e "$blue Installing the newest version"
bash_file/install.sh
clear
